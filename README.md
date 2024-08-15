# arp-spoofer
ARP spoofer with python3

This script allows you to arp spoof a target (a.k.a mitm attack) and act as the victim default gateway, then you can run wireshark or tcpdump and monitor the victim's traffic.

Installation:

1- > git clone https://github.com/BiLLY-J03l/arp-spoofer.git

2- > apt install python3-scapy

3- > chmod +x arp_spoofer.py

4- > ./arp_spoofer.py -t {victim_ip} -d {default_gateway_ip}
