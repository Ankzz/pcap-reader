#!/usr/bin/env python
"""
This module takes care for handling the L3.
Currently just handles the IP Packets.
"""
import dpkt
import sys

from utils.utils import mac_addr
from utils.utils import ip_to_str

from l4.l4_handler import l4_handlers

"""[docs]"""
def ip_packet_handler(lock,ip,counter):
    """IP layer packet handler. Worker thread for analysing IP packet

       Args:
           lock (Lock): Lock to synchronize the thread
           ip (buffer): Buffer of ip header and payload
           counter(int): Integer value specifying the packet number count<Can be done away with>
       Returns:
           None
    """

    with lock:
        print 'Received an ip packet %d'% (counter)

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        # IP information
        srcip = ip.src
        dstip = ip.dst

        # If a L4 parser exists, handle it
        resp = {}
        try:
            resp = l4_handlers[type(ip.data)](ip.data)
        except:
            e = sys.exc_info()[0]
            resp['sport'] = -1
            resp['dport'] = -1

        # For now just print the values
        print "%s:%d::%s:%d:%s" % \
            (ip_to_str(srcip),resp['sport'],ip_to_str(dstip),resp['dport'], type(ip.data))



