#!/usr/bin/env python

import logging
import threading

from utils.bucket import Bucket
import pprint

logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )

class Ip_Flow(object):
    
    def __init__(self):
        self.flows = Bucket()


    def __add__(self, other):
        if type(other)==Bucket:
            self.flows.__add__(other)
        elif type(other)==dict:
            self.flows.__add__(other)


    def __str__(self):
        return self.flows.__str__()


if __name__ == "__main__":
    ## Comes into picture only when executed standalone
    flow = Ip_Flow()

    flow + {99: { 6:7, 7:8 }}
    flow + {99: { 5:7, 7:8 }}

    print flow 
