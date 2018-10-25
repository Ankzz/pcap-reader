#!/usr/bin/env python
"""
Use DPKT to read in a pcap file and print out the contents of the packets
This example is focused on the fields in the Ethernet Frame and IP packet
"""
import dpkt
import datetime
import socket
import threading

from dpkt.ip import IP, IP_PROTO_UDP
from dpkt.udp import UDP
from dpkt.tcp import TCP

from l3.ip_input import ip_packet_handler

from utils.utils import mac_addr
from utils.utils import ip_to_str

import pprint

"""[docs]"""
def print_packets(pcap):
    """Print out information about each packet in a pcap

       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:

        # Print out the timestamp in UTC
        print 'Timestamp: ', str(datetime.datetime.utcfromtimestamp(timestamp))

        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)
        print 'Ethernet Frame: ', mac_addr(eth.src), mac_addr(eth.dst), eth.type

        # Make sure the Ethernet frame contains an IP packet
        # EtherType (IP, ARP, PPPoE, IP6... see http://en.wikipedia.org/wiki/EtherType)
        if eth.type != dpkt.ethernet.ETH_TYPE_IP:
            print 'Non IP Packet type not supported %s\n' % eth.data.__class__.__name__
            continue

        # Now unpack the data within the Ethernet frame (the IP packet) 
        # Pulling out src, dst, length, fragment info, TTL, and Protocol
        ip = eth.data

        # Pull out fragment information (flags and offset all packed into off field, so use bitmasks)
        do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
        more_fragments = bool(ip.off & dpkt.ip.IP_MF)
        fragment_offset = ip.off & dpkt.ip.IP_OFFMASK

        # Print out the info
        print 'IP: %s -> %s   (len=%d ttl=%d DF=%d MF=%d offset=%d)\n' % \
              (ip_to_str(ip.src), ip_to_str(ip.dst), ip.len, ip.ttl, do_not_fragment, more_fragments, fragment_offset)

        # pprint.pprint (ip)

        # Identify ip data type
        if type(ip.data)==UDP:
            udp = ip.data
            pprint.pprint (udp)
        else:
            tcp = ip.data
            pprint.pprint (tcp)
            pprint.pprint (tcp.flags & dpkt.tcp.TH_SYN)


def analyze_packet(pcap):
    """Analyzes each packet and performs DPI

       Args: 
            pcap: ethernet frame received 
    """

    threads = []
    counter = 0
    lock = threading.Lock();

    # Loop through each frame in pcap
    for timestamp, buf in pcap:

        eth = dpkt.ethernet.Ethernet(buf)

        # Not interested in Non-IP Packet
        if eth.type != dpkt.ethernet.ETH_TYPE_IP:
            print 'Non IP Packet'
            continue

        ip = eth.data
        
        # Initiate thread for L4 packet handler 
        t = threading.Thread(target=ip_packet_handler, args=(lock,ip,counter,))
        threads.append(t)
        t.start()
        counter = counter+1


"""[docs]"""
def test():
    """Open up a test pcap file and print out the packets"""
    with open('/Users/ankit_1/pcaps/SynFloodSample.pcap', 'rb') as f:
    #with open('/Users/ankit_1/pcaps/dns.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        analyze_packet(pcap)



if __name__ == '__main__':
    test()