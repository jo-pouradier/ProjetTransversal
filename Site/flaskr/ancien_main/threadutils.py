import multiprocessing
import numpy as np

# custom class wrapping a list in order to make it thread safe
class ThreadSafeList():
    # constructor
    def __init__(self):
        # initialize the list
        self._list = list()
        # initialize the lock
        self._lock = multiprocessing.Lock()

    # add a value to the list
    def append(self, value):
        # acquire the lock
        with self._lock:
            # append the value
            self._list.append(value)

    # extend the list by adding all items of a list to it
    def extend(self, values):
        # acquire the lock
        with self._lock:
            # extend the list
            self._list.extend(values)

    # remove and return the last value from the list
    def pop(self):
        # acquire the lock
        with self._lock:
            # pop a value from the list
            return self._list.pop()
    
    # read a value from the list at an index
    def get(self, index):
        # acquire the lock
        with self._lock:
            # read a value at the index
            return self._list[index]
    
    # return the number of items in the list
    def length(self):
        # acquire the lock
        with self._lock:
            return len(self._list)
        
# custom class wrapping a frame in order to make it thread safe
class ThreadSafeFrame():
    def __init__(self, max_size):
        #create byte array of size array_size
        self.max_size = max_size
        self.current_size = max_size
        # create a bytes object multiprocess safe
        self.array = multiprocessing.RawArray('B', [0]*self.max_size)
        self._lock = multiprocessing.Lock()
    
    def setFrame(self, frame):
        with self._lock:
            #convert image to flattened array
            self.current_size = len(frame)
            if self.current_size > self.max_size:
                # reencode the frame to a smaller size
                print(f"WARNING: Frame size ({self.current_size})exceeds max size ({self.max_size}). Truncating frame.")
                self.current_size = self.max_size
            self.array[:self.current_size] = frame[:self.current_size]
    
    def getFrame(self):
        with self._lock:
            return bytes(self.array[:self.current_size])
        
# custom class wrapping a dictionary in order to make it thread safe
class ThreadSafeDict():
    def __init__(self):
        # create en multiprocessing dictionary
        self._dict = multiprocessing.Manager().dict()
        self._lock = multiprocessing.Lock()
    
    def set(self, key, value):
        with self._lock:
            self._dict[key] = value
    
    def get(self, key):
        with self._lock:
            return self._dict[key]
    
    def keys(self):
        with self._lock:
            return self._dict.keys()

    def values(self):
        with self._lock:
            return self._dict.values()
    
    def items(self):
        with self._lock:
            return self._dict.items()
    
    def __getitem__(self, key):
        with self._lock:
            return self._dict[key]
        
    def __setitem__(self, key, value):
        with self._lock:
            self._dict[key] = value
    
    def __contains__(self, key):
        with self._lock:
            return key in self._dict
    
    def __len__(self):
        with self._lock:
            return len(self._dict)
    
    def __repr__(self):
        with self._lock:
            return self._dict.__repr__()
    
    def __str__(self):
        with self._lock:
            return self._dict.__str__()
        
    def __iter__(self):
        with self._lock:
            return self._dict.__iter__()
        
    def __next__(self):
        with self._lock:
            return self._dict.__next__()
        
    def __delitem__(self, key):
        with self._lock:
            return self._dict.__delitem__(key)
    
    def __copy__(self):
        with self._lock:
            return self._dict.__copy__()

    def __deepcopy__(self, memo):
        with self._lock:
            return self._dict.__deepcopy__(memo)
    
    def __eq__(self, other):
        with self._lock:
            return self._dict.__eq__(other)
    
    def __ne__(self, other):
        with self._lock:
            return self._dict.__ne__(other)
    
    def __ge__(self, other):
        with self._lock:
            return self._dict.__ge__(other)
    
    def __gt__(self, other):
        with self._lock:
            return self._dict.__gt__(other)
        
    def __le__(self, other):
        with self._lock:
            return self._dict.__le__(other)
        
    def __lt__(self, other):
        with self._lock:
            return self._dict.__lt__(other)
    
    def __hash__(self):
        with self._lock:
            return self._dict.__hash__()
        
    def __sizeof__(self):
        with self._lock:
            return self._dict.__sizeof__()
