#!/usr/bin/env python

from dpkt.udp import UDP
from dpkt.tcp import TCP

from tcp_handler import tcp_packet_handler
from udp_handler import udp_packet_handler

l4_handlers = {
    TCP : tcp_packet_handler,
    UDP : udp_packet_handler,
}
