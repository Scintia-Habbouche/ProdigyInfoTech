import os
import sys
from scapy.all import  sniff, IP, TCP, UDP

# Disclaimer and terms of use
print("------------------------ Packet Sniffer Tool Disclaimer ---------------------------")
print("This packet sniffer tool is intended for educational and ethical purposes only.")
print("Unauthorized use, distribution, or modification of this tool is strictly prohibited.")
print("By using this tool, you agree to the following terms and conditions:")
print("\n1. You will only use this tool on networks and systems for which you have explicit permission.")
print("2. You will not use this tool to violate any laws, regulations, or terms of service.")
print("3. You will not use this tool to harm, disrupt, or exploit any networks or systems.")
print("4. You will not use this tool to intercept, collect, or store any sensitive or confidential information.")
print("5. You will not redistribute or sell this tool without the express permission of the author.")
print("6. The author is not responsible for any damages or losses incurred as a result of using this tool.")
print("7. You will respect the privacy and security of all networks and systems you interact with using this tool.")

accept_terms = input("\nDo you accept these terms and conditions? (y/n): ")

if accept_terms.lower() != 'y':
    print("You must accept the terms and conditions before using this tool.")
    sys.exit()

print("\n--------------- Packet Sniffing Tool ---------------")

# Prompt user for filter and packet count
custom_filter = input("Enter a BPF filter (e.g., 'tcp', 'udp', 'icmp' or leave blank for all): ")
packet_count = int(input("Enter the number of packets to capture (0 for unlimited): "))

# Function to display and save captured packets
def packet_sniff(packet):
    try:
        # Check if the packet has an IP layer
        if packet.haslayer(IP):
            src_ip = packet[IP].src       # Source IP address
            dst_ip = packet[IP].dst       # Destination IP address
            protocol = packet[IP].proto   # Protocol type (TCP, UDP, etc.)
            timestamp = packet.time       # Timestamp of the packet capture

            # Prepare output string with basic packet information
            output_string = f"Timestamp: {timestamp}\n"
            output_string += f"Source IP: {src_ip}\n"
            output_string += f"Destination IP: {dst_ip}\n"
            output_string += f"Protocol: {protocol}\n"

            # Check if the packet has a TCP layer and extract additional information if present
            if packet.haslayer(TCP):
                src_port = packet[TCP].sport          # Source TCP port
                dst_port = packet[TCP].dport          # Destination TCP port
                output_string += f"Source Port: {src_port}\n"
                output_string += f"Destination Port: {dst_port}\n"
                payload = str(packet[TCP].payload)    # TCP payload data (if any)
                output_string += f"Payload (first 50 chars): {payload[:50]}...\n"  # Display the first 50 characters of payload

            # Check if the packet has a UDP layer and extract additional information if present
            elif packet.haslayer(UDP):
                src_port = packet[UDP].sport          # Source UDP port
                dst_port = packet[UDP].dport          # Destination UDP port
                output_string += f"Source Port: {src_port}\n"
                output_string += f"Destination Port: {dst_port}\n"
                payload = str(packet[UDP].payload)    # UDP payload data (if any)
                output_string += f"Payload (first 50 chars): {payload[:50]}...\n"  # Display the first 50 characters of payload
            
            # Print the output to the console and save it to a file
            print(output_string, end='')
            with open(output_file, 'a') as f:
                f.write(output_string + "\n" + "-"*50 + "\n")

    except Exception as e:
        print(f"Error processing packet: {e}")

# Set the path and filename for the output text file
output_file = "packet_sniffer_results.txt"

# Display the output file's name and location after successful sniffing
print(f"\nSniffing started... Saving results to: {output_file}")
print("Press Ctrl+C to stop...\n")

# Sniff packets with user-defined filter and packet count
sniff(filter=custom_filter, prn=packet_sniff, store=0, count=packet_count)
