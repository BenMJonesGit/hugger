from scapy.all import rdpcap
import sys

def read_pcap(file_path):
    packets = rdpcap(file_path)

    for packet in packets:
        print(packet)
        if packet.haslayer('IP'):
            # Extracting IP addresses and ports
            src_ip = packet['IP'].src
            dst_ip = packet['IP'].dst

            src_port = packet['TCP'].sport if packet.haslayer('TCP') else packet['UDP'].sport if packet.haslayer('UDP') else None
            dst_port = packet['TCP'].dport if packet.haslayer('TCP') else packet['UDP'].dport if packet.haslayer('UDP') else None

            # Extracting timestamp
            timestamp = packet.time

            print(f"Timestamp: {timestamp}, Source IP: {src_ip}, Destination IP: {dst_ip}, Source Port: {src_port}, Destination Port: {dst_port}")

if __name__ == "__main__":
    # Replace 'sample.pcap' with the path to your pcap file
    print(sys.argv[1])
    read_pcap(sys.argv[1])
