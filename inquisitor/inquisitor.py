import argparse
import libpcap
# import scapy.all import *

parser = argparse.ArgumentParser(description="Perform ARP poisoning on a target")
parser.add_argument("ip_src", help="Enter the ip address of the source machine")
parser.add_argument("mac_src", help="Enter the mac address of the source machine")
parser.add_argument("ip_target", help="Enter the ip address of the target machine")
parser.add_argument("mac_target", help="Enter the mac address of the target machine")

# send(IP(dst="")/ARP())

args = parser.parse_args()
