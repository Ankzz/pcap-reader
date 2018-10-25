#!/usr/bin/env python

import dpkt
import sys

import pprint

def getAllInterfaces():
    devices = dpkt.pcap.findalldevs()
    pprint.pprint(devices)

if __name__ == '__main__':
    getAllInterfaces()
