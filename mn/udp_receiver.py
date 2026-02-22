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

