#!/usr/bin/env python

import dpkt

"""[docs]"""
def tcp_packet_handler(tcp):
    """TODO: Add Code for tcp """
    #print 'Received a tcp packet'
    #pprint.pprint(tcp)

    resp = {}
    resp['sport'] = tcp.sport
    resp['dport'] = tcp.dport

    return resp

