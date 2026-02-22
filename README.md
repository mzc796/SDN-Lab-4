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
4. Send UDP packets from Host 1 and let Host 2 listen to the incoming packets
   
   (1) Open hosts' terminals. In the mininet terminal:
   ```
   xterm h1 h2
   ```
   You should see two black terminals coming out. They are the `h1` and `h2`.
   
   (2) In the `h1` terminal:
   ```
   python3 udp_sender.py
   ```
   (3) Let Host 2 listen to the incoming packets
   In the `h2` terminal:
   ```
   python3 udp_receiver.py
   ```
   Question: Did the `h2` receive anything? Why? How do you verify that `h1` has successfully sent packets?
   
   (4) Make `h2` receive packets from `h1` successfully
   Refer to [OpenDaylight Flow Examples](https://docs.opendaylight.org/projects/openflowplugin/en/latest/users/flow-examples.html)
   
5. Establish a TCP connection between Host 1 and Host 2
   
   (1) In the `h2` terminal:
   ```
   python3 tcp_server.py
   ```
   (2) In the `h1` terminal:
   ```
   python3 tcp_client.py
   ```
   Question: Is the TCP connection successful? Why?
   
   (3) Make the TCP connection successful.
   
6. Now, only use 1 flow entry on each switch to forward both UDP and TCP packets.
   
7. Start another TCP connection between Host 1 and Host 2. Support switch 1 is the monitor, set one flow entry to forward the packets of this connection to the controller.
