from pcapfile import savefile
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
import binascii

testcap = open('/Users/ankit_1/pcaps/dns.pcap', 'rb')

capfile = savefile.load_savefile(testcap, verbose=False)

eth_frame = ethernet.Ethernet(capfile.packets[0].raw())

ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))

print ip_packet

