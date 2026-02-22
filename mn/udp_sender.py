from scapy.all import *
import time

dst_ip = "10.0.0.2"   # h2 IP
src_ip = "10.0.0.1"   # h1 IP

print("Sending custom IPv4 packets to", dst_ip)

for i in range(5):
    pkt = IP(src=src_ip, dst=dst_ip) / UDP(sport=1234, dport=4321) / Raw(load=f"Message {i}")
    send(pkt, verbose=False)
    print("Sent packet", i)
    time.sleep(1)

print("Done.")

