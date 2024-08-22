#!/bin/env python

import collections.abc
import getpass

import requests
import msgpack
import msgpack_numpy as mn
import numpy as np

# Allow disabling SSL certificate verification and associated warnings (useful for testing)
verify_cert = True
def disable_verify_cert():
    global verify_cert
    import urllib3
    urllib3.disable_warnings()
    verify_cert = False

# Will store session objects between requests
session = None

# Default maximum recursion depth when loading nested groups in a single
# request. Deeper groups are only loaded when requested.
max_depth_default = 1

# Default maximum size in bytes of dataset contents to load with the parent
# group. Larger datasets are only loaded when sliced.
data_size_limit_default = 64*1024


def auth(server, user=None, password=None):
    """
    Create a session object with credentials and check that they work.
    """
    global session

    # Remove any trailing slashes from the server name
    server = server.rstrip("/")
    
    # Set up a session with the username and password
    if user is None:
        user = getpass.getpass("User: ")
    if password is None:
        password = getpass.getpass("Password: ")
    new_session = requests.Session()
    new_session.auth = (user, password)

    # Test credentials by fetching a directory listing
    response = new_session.get(server+"/msgpack/FLAMINGO", verify=verify_cert)
    raise_for_status(response)

    # Request worked, so store the session
    session = new_session

    
def decode_hook(data):
    """
    Converts dicts decoded from the msgpack stream into numpy ndarrays. Called
    by msgpack.unpack().

    Dicts with nd=True contain a binary buffer which should be wrapped with a
    numpy array with type and shape given by the metadata in the dict. We call
    msgpack-numpy's decode() function to do this.
    
    Dicts with vlen=True contain flattened lists of variable size
    elements and are translated into numpy object arrays.
    """
    # If this is a serialized ndarray, use msgpack-numpy to decode it
    data = mn.decode(data)

    # Then check for any vlen data: in that case we have a flattened list
    # which needs to be converted into an object array of the right shape.
    if isinstance(data, dict):
        if b"vlen" in data:
            # Get the shape of the array
            shape = [int(i) for i in data[b"shape"]]
            if len(shape) == 0:
                # For scalars, just return the value
                data = data[b"data"][0]
            else:
                # Otherwise we make an object array
                arr = np.empty(len(data[b"data"]), object)
                arr[:] = data[b"data"]
                data = arr.reshape(shape) 
    return data


class HDFStreamRequestError(Exception):
    pass


def raise_for_status(response):
    """
    Check the http response status and raise an exception if necessary

    This also extracts the error message from the response body, if
    there is one.
    """
    if not response.ok:
        if response.status_code == 401:
            # Catch case of wrong password
            raise HDFStreamRequestError("Not authorized. Incorrect username or password?")
        try:
            # Extract msgpack encoded error string from response
            data = msgpack.unpack(response.raw)
            message = data["error"]
        except Exception:
            # If we don't have a message from the server, let the requests
            # module generate an exception
            response.raise_for_status()
        else:
            # Raise an exception using the error message
            raise HDFStreamRequestError(message)

    
def request_object(url, name, max_depth, data_size_limit):
    """
    Download the msgpack representation of a HDF5 object
    """
    params = {"object" : name, "data_size_limit" : data_size_limit, "max_depth" : max_depth}
    with session.get(url, params=params, stream=True, verify=verify_cert) as response:        
        raise_for_status(response)
        data = msgpack.unpack(response.raw, object_hook=decode_hook)
    return data


def unpack_object(url, name, data, max_depth, data_size_limit):
    """
    Construct an appropriate class instance for a HDF5 object
    """
    object_type = data[b"hdf5_object"]
    if object_type == b"group":
        return RemoteGroup(url, name, max_depth, data_size_limit, data)
    elif object_type == b"dataset":
        return RemoteDataset(url, name, data)
    else:
        raise RuntimeError("Unrecognised object type")
    

class RemoteDataset:
    """
    Object representing a HDF5 dataset in the remote file    
    """
    def __init__(self, url, name, data):

        self.url = url
        self.name = name
        self.attrs = data[b"attributes"]
        self.dtype = np.dtype(data[b"type"])
        self.kind  = data[b"kind"]
        self.shape = tuple(data[b"shape"])
        if b"data" in data:
            self.data = data[b"data"]
        else:
            self.data = None

        for name in self.attrs:
            self.attrs[name] = self.attrs[name]
            
    def _single_slice(self, start, count):
        """
        Fetch a slice of this dataset. May return fewer elements
        than requested if result is too large for a msgpack bin
        object.

        start: array of starting offsets in each dimension
        count: number of elements to fetch in each dimension
        """        
        params = {
            "object" : self.name,
            "start"  : ",".join([str(int(i)) for i in start]),
            "count"  : ",".join([str(int(i)) for i in count]),
            }

        with session.get(self.url, params=params, stream=True, verify=verify_cert) as response:        
            raise_for_status(response)
            data = msgpack.unpack(response.raw, object_hook=decode_hook)
            
        return data

    def slice(self, start, count):
        """
        Repeatedly slice dataset until all requested elements
        have been received.
        """
        current_start = np.asarray(start, dtype=int).copy()
        current_count = np.asarray(count, dtype=int).copy()
        
        data = []
        while True:
            data.append(self._single_slice(current_start, current_count))
            if len(current_count) > 0:
                nr_read = data[-1].shape[0]
                current_count[0] -= nr_read
                current_start[0] += nr_read
                if current_count[0] == 0:
                    break
        return np.concatenate(data, axis=0)
        
    def __getitem__(self, key):
        """
        Fetch a dataset slice by indexing this object.

        Translates a numpy style tuple of integer/slice/ellipsis objects into
        the start and count parameters needed for the web API.
        """
        
        # Ensure key is at least a one element sequence
        if not isinstance(key, collections.abc.Sequence):
            key = (key,)
            
        start = []
        count = []
        dim_nr = 0
        found_ellipsis = False
        result_dim = []
        for k in key:
            if isinstance(k, int):
                # This is a single integer index
                start.append(k)
                count.append(1)
                dim_nr += 1
            elif isinstance(k, slice):
                # This is a slice. Step must be one, if specified.
                if k.step != 1 and k.step != None:
                    raise KeyError("RemoteDataset slices with step != 1 are not supported")
                # Find start and stop parameters
                slice_start = k.start if k.start is not None else 0
                slice_stop = k.stop if k.stop is not None else self.shape[dim_nr]
                start.append(slice_start)
                count.append(slice_stop-slice_start)
                dim_nr += 1
                result_dim.append(count[-1])
            elif k is Ellipsis:
                # This is an Ellipsis. Selects all elements in as many dimensions as needed.
                if found_ellipsis:
                    raise KeyError("RemoteDataset slices can only contain one Ellipsis")
                ellipsis_size = len(self.shape) - len(key) + 1
                if ellipsis_size < 0:
                    raise KeyError("RemoteDataset slice has more dimensions that the dataset")
                for i in range(ellipsis_size):
                    start.append(0)
                    count.append(self.shape[dim_nr])
                    dim_nr += 1
                    result_dim.append(count[-1])
                found_ellipsis = True
            else:
                raise KeyError("RemoteDataset index must be integer or slice")

        if self.data is None:
            # Dataset is not in memory, so request it from the server
            data = self.slice(start, count)
            # Remove any dimensions where the index was a scalar, for
            # consistency with numpy
            data = data.reshape(result_dim)
            # In case of scalar results, don't wrap in a numpy scalar
            if isinstance(data, np.ndarray):
                if len(data.shape) == 0:
                    return data[()]
            return data
        else:
            # Dataset was already loaded with the metadata
            return self.data[key]

    def __repr__(self):
        return f'<Remote HDF5 dataset "{self.name}" shape {self.shape}, type "{self.dtype.str}">'

    
class RemoteGroup(collections.abc.Mapping):
    """
    Object representing a HDF5 group in the remote file
    """
    def __init__(self, url, name, max_depth=max_depth_default,
                 data_size_limit=data_size_limit_default, data=None):

        self.url = url
        self.name = name
        self.max_depth = max_depth
        self.data_size_limit = data_size_limit
        self.unpacked = False

        # If msgpack data was supplied, decode it. If not, we'll wait until
        # we actually need the data before we request it from the server.
        if data is not None:
            self.unpack(data)
            
    def load(self):
        """
        Request the msgpack representation of this group from the server
        """
        if not self.unpacked:
            data = request_object(self.url, self.name, self.max_depth, self.data_size_limit)
            self.unpack(data)
            
    def unpack(self, data):
        """
        Decode the msgpack representation of this group
        """
        # Store any attributes
        self.attrs = data[b"attributes"]
        for name in self.attrs:
            self.attrs[name] = self.attrs[name]

        # Create sub-objects
        self.members = {}
        if b"members" in data:
            for member_name, member_data in data[b"members"].items():
                if member_data is not None:                    
                    if self.name == "/":
                        path = self.name + member_name
                    else:
                        path = self.name + "/" + member_name
                    self.members[member_name] = unpack_object(self.url, path, member_data, self.max_depth, self.data_size_limit)
                else:
                    self.members[member_name] = None

        self.unpacked = True
                    
    def ensure_member_loaded(self, key):
        """
        Load sub-groups on access, if they were not already loaded
        """
        self.load()
        if self.members[key] is None:
            object_name = self.name+"/"+key
            self.members[key] = RemoteGroup(self.url, object_name, self.max_depth, self.data_size_limit)
                                
    def __getitem__(self, key):
        """
        Return a member object identified by its name or relative path.

        If the key is a path with multiple components we use the first
        component to identify a member object to pass the rest of the path to.
        """
        self.load()
        if key != "/":
            key = key.rstrip("/")
        components = key.split("/", 1)
        if len(components) == 1:
            self.ensure_member_loaded(key)
            return self.members[key]
        else:
            self.ensure_member_loaded(components[0])
            return self[components[0]][components[1]]

    def __len__(self):
        self.load()
        return len(self.members)

    def __iter__(self):
        self.load()
        for member in self.members:
            yield member

    def __repr__(self):
        if self.unpacked:
            return f'<Remote HDF5 group "{self.name}" ({len(self.members)} members)>'
        else:
            return f'<Remote HDF5 group "{self.name}" (to be loaded on access)>'
        

class RemoteDirectory(collections.abc.Mapping):
    """
    Object representing a virtual directory on the remote server
    """
    def __init__(self, server, name, user=None, password=None, data=None,
                 max_depth=max_depth_default, data_size_limit=data_size_limit_default,
                 lazy_load=False):

        # Remove any trailing slashes from the server name
        server = server.rstrip("/")

        # Remove any trailing slashes from the directory name
        name = name.rstrip("/")
        
        # Set up a new session if necessary. May need to ask for password.
        global session
        if session is None:
            auth(server, user, password)

        # Store the server URL etc
        self.server = server
        self.data_size_limit = data_size_limit
        self.max_depth = max_depth
        self.name = name
        self.unpacked = False
        
        # If msgpack data was supplied, decode it. If not, we'll wait until
        # we actually need the data before we request it from the server.
        if data is not None:
            self.unpack(data)

        # If the class was explicitly instantiated by the user (and not by a
        # recursive unpack() call) then we should always contact the server so
        # that we immediately detect incorrect paths.
        if lazy_load==False and not(self.unpacked):
            self.load()
            
    def load(self):
        """
        Request the msgpack representation of this directory from the server
        """
        if not self.unpacked:
            url = f"{self.server}/msgpack/{self.name}"
            with session.get(url, stream=True, verify=verify_cert) as response:        
                raise_for_status(response)
                data = msgpack.unpack(response.raw, object_hook=mn.decode)
            self.unpack(data)
            self.unpacked = True
            
    def unpack(self, data):
        """
        Decode the msgpack representation of this directory
        """        
        # Store dict of files in this directory
        self._files = {}
        for filename in data["files"]:
            path = self.name + "/" + filename
            url = f"{self.server}/msgpack/{path}"
            self._files[filename] = RemoteGroup(url, "/", max_depth=self.max_depth, data_size_limit=self.data_size_limit)

        # Store dict of subdirectories in this directory
        self._directories = {}
        for subdir_name, subdir_data in data["directories"].items():
            subdir_object = RemoteDirectory(self.server, self.name+"/"+subdir_name, data=subdir_data, lazy_load=True)
            self._directories[subdir_name] = subdir_object
            
    def __getitem__(self, key):

        # Request directory listing from the server if necessary
        self.load()

        # Remove any trailing slash
        if key != "/":
            key = key.rstrip("/")
        
        # Check for the case where key refers to something in a sub-directory
        components = key.split("/", 1)
        if len(components) > 1:
            return self._directories[components[0]][components[1]]

        # Check if key refers to a subdirectory in this directory
        name = components[0]
        if name in self._directories:
            return self._directories[name]
        
        # Check if key refers to a file in this directory
        if name in self._files:
            return self._files[name]

        raise KeyError("Invalid path: "+key)
        
    def __len__(self):
        self.load()
        return len(self._directories) + len(self._files)

    def __iter__(self):
        self.load()
        for directory in self._directories:
            yield directory
        for file in self._files:
            yield file

    def __repr__(self):
        self.load()
        nr_files = len(self._files)
        nr_dirs = len(self._directories)
        return f'<Remote directory {self.name} with {nr_dirs} sub-directories, {nr_files} files>'

    @property
    def files(self):
        self.load()
        return self._files

    @property
    def directories(self):
        self.load()
        return self._directories
