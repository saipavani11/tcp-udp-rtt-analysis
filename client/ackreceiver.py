import socket
import time
import random

server_ip = input("Enter server IP: ").strip()
server_address = (server_ip, 5555)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(2)  # Timeout for ACKs

seq_num = 1  # Start sequence number

while True:
    message = input("Enter message (or 'exit' to disconnect): ")
    if message.lower() == "exit":
        client_socket.sendto(f"{seq_num}:exit".encode(), server_address)
        print("🔴 Disconnected from server.")
        break

    send_time = time.time()
    full_message = f"{seq_num}:{send_time}:{message}"

    # 🔥 Simulate 20% packet loss
    if random.random() > 0.2:
        client_socket.sendto(full_message.encode(), server_address)
        print(f"📤 Sent Packet {seq_num}: '{message}'")
    else:
        print(f"❌ Simulated Packet Drop - Packet {seq_num}")

    # 🔄 Wait for ACK and Resend if not received
    try:
        ack, _ = client_socket.recvfrom(1024)
        ack_num = int(ack.decode())
        print(f"✅ ACK Received for Packet {ack_num}")
        seq_num += 1  # Move to next sequence number
    except socket.timeout:
        print(f"⚠️ No ACK for Packet {seq_num} - Resending...")
        continue  # Resend the same packet

client_socket.close()
