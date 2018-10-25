import logging
import threading

import pprint

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

class Bucket(object):

    def __init__(self):
        super(Bucket, self).__init__()
        self.bucket = {}
        self.lock = threading.Lock()

        
    def add(self, key, value):
        logging.debug("Adding %s to the bucket", key)

        with self.lock:
            if key in self.bucket:
                # Here I need to update the bucket members
                self.bucket[key] = value
            else:
                # Add the item to the bucket
                self.bucket[key] = value
                

    def __add__(self, other):
        logging.debug("Adding %s to the bucket",type(other))

        # Only dictionary/bucket type can be added
        if type(other)==dict:
            logging.debug("Adding dict to the bucket")
            existing = {k: v for k,v in other.iteritems() if k in self.bucket}
            other = {k: v for k,v in other.iteritems() if k not in self.bucket }
       
            for k, v in other.iteritems():
                self.add(k, v)
            if bool(existing):
                for x,y in existing.iteritems():
                    self.add(x, y)

        elif type(other)==Bucket:
            logging.debug("Adding Bucket to the bucket")
            self.bucket.update(other.bucket)
        else:
            logging.error("Adding non-dictionary/non-Bucket item to the bucket")
            # Should throw an exception here 


    def __radd__(self, other):
        # Dictionary so order does not matters
        self.__add__(other)


    def __sub__(self, other):
        logging.debug("Deleting %s from the bucket", type(other))

        if type(other)==int or type(other)==str:
            with self.lock:
                if other in self.bucket: 
                    del self.bucket[other]
           

    def __format__(self):
        logging.debug("Call for formatting")
        with self.lock:
            return '{}{}'.format(**self.bucket)

 
    def __str__(self):
        with self.lock:
            return self.bucket.__str__()


    def get(self):
        with self.lock:
            return self.bucket


    def getitem(self, key=None):
        if key!=None:
            with self.lock:
                if key in self.bucket:
                    return self.bucket[key]
                else:
                    return None
        else:
            return self.get()

    def __getitem__(self, key=None, itemkey=None):
        if itemkey!=None:
            with self.lock:
                if key in self.bucket:
                    if type(self.bucket[key])==dict and itemkey in self.bucket[key]:
                        return self.bucket[key][itemkey]
                    else:
                        return None
                else:
                    return None
        else:
            return self.getitem(key)

    def setitem(self, key, value):
        with self.lock:
            if key in self.bucket:
                self.bucket[key] = value
                # Do I need an else for this


    def __setitem__(self, key, value, subkey=None):

        if subkey!=None:
            with self.lock:
                if key in self.bucket:
                    if type(self.bucket[key])==dict:
                        if subkey in self.bucket[key]:
                            self.bucket[key][subkey]=value;
                        else:
                            self.bucket[key][subkey]=value;
                    else:
                        #Need to throw an exception for NoSuchSubKey here
                        logging.error("bucket key value not a dictionary item")
                else:
                    #Need to throw an exception here for NoSuchKey here
                    logging.error("Key does not exists in bucket")
        else:
            self.setitem(key, value)
                    
if (__name__ == "__main__"):
    """ This is test code. Does not commeth in picture while running """

    b = Bucket()
    x = Bucket()

    # Adding item to bucket using add method
    print "# Adding item to bucket using add method"
    b.add(5, {'hello': 'world', 'details': { 'map': 0, 'zap': '0' }})

    # Adding a dictionary to a bucket
    p = {99: { 6:7, 7:8 }}
    b + p
    print "# Adding a dictionary to a bucket"
    print b


    # Updating the same key using a dictionary object
    p = {99: { 5:8, 7:8 }}
    p + b
    print "# Updating the same key using a dictionary object"
    print b

    # Fetch key value
    print b[0]
    print b[99]

    p = {98: { 1:2, 3:4, 5:6 }}
    
    p + x 
    # Adding a new key using addition of two buckets
    b + x
    print "# Adding a new key using addition of two buckets"
    print b

    # Updating using array nomenclature
    b[5] = x
    print "# Updating using array nomenclature"
    print b

    # Updating a subkey value
    print "# Updating a subkey value"
    b[5]['hello']='worlds'
    xyz =  b[5]
    print type(xyz)
    print b

    b - 5
    print b
