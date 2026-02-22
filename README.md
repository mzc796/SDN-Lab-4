# SDN-Lab-4
Practise flow entry setup

Continue with SDN-Lab-3, we send various packet types from hosts and configure corresponding flow entries on the switches. 
## Virtual Machine Summary
Memory: >= 8GB

Storage: 50GB

CPU: 2 cores, AMD64 Architecture

Installation Disc: [ubuntu-22.04.4-desktop-amd64.iso](https://old-releases.ubuntu.com/releases/22.04/)

## References
[An Instant Virtual Network on your Laptop (or other PC)](https://mininet.org/)

[PICOS 4.4.3 Configuration G](https://pica8-fs.atlassian.net/wiki/spaces/PicOS443sp/overview?homepageId=10453009)

[OpenDaylight Flow Examples](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/flow-examples.html)
## Start SDN testbed
1. Open a terminal, start OpenDaylight:
   ```
   cd karaf-0.20.1/bin
   sudo ./karaf
   ```
2. Open another terminal, start Mininet. :
   ```
   sudo run_mn.sh
   ```
   
3. Install xterm and python3-scapy:
   ```
   sudo apt update
   sudo apt install xterm
   sudo apt install -y python3-scapy
   ```
   Verify:
   ```
   python3 -c "from scapy.all import *; print('Scapy OK')"
   ```
4. Write IPv4 sender and receiver in Python with Scapy
   ```
   vim sender.py
   ```
   Copy & paste the code into the `sender.py`:
   ```
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
   ```
   ```
   vim receiver.py
   ```
   Copy & paste the code into the `receiver.py`
   ```
   from scapy.all import sniff, conf, hexdump

   IFACE = "h2-eth0"
   
   def handle(pkt):
       print("=== got packet ===")
       print(pkt.summary())
       try:
           pkt.show()
       except Exception as e:
           print("show() failed:", e)
       # Uncomment if you want raw bytes:
       # hexdump(pkt)
   
   print("Scapy version OK. Sniffing on", IFACE)
   print("conf.iface =", conf.iface)
   sniff(iface=IFACE, filter="udp", prn=handle, store=False)
   #sniff(iface=IFACE, prn=handle, store=False)

   ```
5. Send IP packets from Host 1 and let Host 2 listen to the incoming packets
   (1) Open hosts' terminals. In the mininet terminal:
   ```
   xterm h1 h2
   ```
   You should see two black terminals coming out. They are the `h1` and `h2`.
   
   (2) In the `h1` terminal:
   ```
   sudo python3 sender.py
   ```
   (3) Let Host 2 listen to the incoming packets
   In the `h2` terminal:
   ```
   sudo python3 receiver.py
   ```
   Question: Did the `h2` receive anything? Why? How do you verify that `h1` has successfully sent packets?
   
   (4) Make `h2` receive packets from `h1` successfully
   Refer to [OpenDaylight Flow Examples](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/flow-examples.html)
