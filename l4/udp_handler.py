#!/usr/bin/env python

import dpkt

"""[docs]"""
def udp_packet_handler(udp):
    """TODO: Add Code for udp """
    print 'Received a udp packet'
    #pprint.pprint(udp)

    resp = {}
    resp['sport'] = udp.sport
    resp['dport'] = udp.dport

    return resp

