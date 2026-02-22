# SDN-Lab-3
Configure flow entries via OpenDaylight northbound interface

Continue with SDN-Lab-2, now let's configure flow entries via the OpenDaylight northbound interface 
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
3. Open the 3rd terminal to request nodes to verify the connection:
   ```
   cd odl/
   mkdir data
   sudo ./req_nodes.sh
   ```
   Read the file `data/nodes.json`. If it has statistics, the connection is successful.
   
4. Try `ping`. In the mininet terminal:
   ```
   h1 ping h2
   ```
   Question: Was the `ping` successful? Why?
   
5. Use OpenDaylight Rest API to configure ARP flow entries

   (1) Refer to `odl/arp_odl.sh` to configure the ARP flow entries for each switch.
   
   NOTE: The format of dest IP address is `10.0.0.1/32`. Search what does `10.0.0.1/32` mean?

   (2) Request the config data store on the OpenDaylight. On a terminal:
   ```
   cd odl/
   sudo ./req_config_flows.sh $SW_ID
   vim data/$SW_ID_config_flows.json
   ```
   If the json file has content as expected, the flow entry is configured successfully.

   (3) Check the flow entry on the mininet. On a terminal:
   ```
   cd mn/
   sudo ./dump-flows.sh $SW_ID
   ```

   If the flow entry is indeed on the mininet switch, this configuration is successful.

   (4) Finish the flow entries on both switches to enable complete ARP packet exchanges.

   (5) On the mininet terminal, check arp table on both host, e.g.,
   ```
   h1 arp
   ```
   Continue until `h1 arp` and `h2 arp` have complete arp tables.
   
6. Use OpenDaylight Rest API to configure ICMP flow entries
   
   (1) Refer to `odl/icmp_odl.sh` to configure ICMP flow entries for each switch.

   (2) Finish the flow entries on both switches to enable complete ICMP packet exchanges, until `h1 ping h2` is successful.

7. Understand the config and nonconfig data store
   
   (1) Shut down OpenDaylight with `control + D`. Restart mininet and read flow entries on the mininet end. Keep in mind your observation.

   (2) Restart OpenDaylight. Read flow entries on the mininet end.
   
   Question: What do you observe? Why?

8. Practice flow entry setup with [examples](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/flow-examples.html)
   
   (1) Install xterm and python3:
   ```
   sudo apt update
   sudo apt install xterm
   sudo apt install -y python3-scapy
   ```
   Verify:
   ```
   python3 -c "from scapy.all import *; print('Scapy OK')"
   ```
   (2) Write IPv4 sender and receiver in Python with Scapy
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
   (3) Open hosts' terminals. In the mininet terminal:
   ```
   xterm h1 h2
   ```
   You should see two black terminals coming out. They are the `h1` and `h2`.
   
   (4) Send IP packets from Host 1 
   In the `h1` terminal:
   ```
   sudo python3 sender.py
   ```
   (5) Let Host 2 listen to the incoming packets
   In the `h2` terminal:
   ```
   sudo python3 receiver.py
   ```
   Question: Did the `h2` receive anything? Why? How do you verify whether `h1` has sent packets successfully?
   
   (6) Make `h2` receive packets from `h1` successfully
   Refer to [OpenDaylight Flow Examples](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/flow-examples.html)
