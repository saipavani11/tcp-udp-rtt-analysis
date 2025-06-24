import socket
import time
import random

def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_ip = input("Enter server IP: ").strip()
    server_address = (server_ip, 5555)

    seq_num = 1  # Sequence number starts at 1
    session_start_time = time.time()

    while True:
        message = input("Enter message (type 'exit' to quit): ")
        if message.lower() == "exit":
            client_socket.sendto(f"{seq_num}:{time.time()}:exit".encode(), server_address)
            break

        send_time = time.time()
        full_message = f"{seq_num}:{send_time}:{message}"

        # 🔥 Simulate Packet Drop: Skip sending 20% of packets
        if random.random() > 0.2:  # 80% chance of sending
            client_socket.sendto(full_message.encode(), server_address)
            print(f"📤 Sent Packet {seq_num}: '{message}'")
        else:
            print(f"❌ Simulated Packet Drop - Packet {seq_num}")

        seq_num += 1
        time.sleep(1)

    total_session_time = time.time() - session_start_time
    print(f"\n🔴 Session Ended. Total Duration: {total_session_time:.4f} sec\n")

if __name__ == "__main__":
    udp_client()
