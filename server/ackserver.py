import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 5555))
print("🚀 Server is running on port 5555...")

clients = {}  # Track expected sequence numbers for each client

def handle_client():
    while True:
        try:
            data, addr = server_socket.recvfrom(1024)
            decoded = data.decode()

            # Extract sequence number and message
            parts = decoded.split(":")
            if len(parts) < 2:
                continue

            seq_num = int(parts[0])
            message = parts[2] if len(parts) > 2 else "exit"

            # Initialize expected sequence number for new clients
            if addr not in clients:
                clients[addr] = 1

            # 🔥 Detect and Log Packet Drop
            expected_seq = clients[addr]
            if seq_num > expected_seq:
                missing_packets = seq_num - expected_seq
                print(f"⚠️ Packet Drop Detected from {addr}! Expected {expected_seq}, but received {seq_num} (Dropped {missing_packets} packets)")

            # ✅ Process Correct Packet
            print(f"📩 Received Packet {seq_num} from {addr} | Message: '{message}'")
            clients[addr] = seq_num + 1  # Update expected sequence number

            # Handle client disconnection
            if message.lower() == "exit":
                print(f"🔴 Client {addr} disconnected.")
                del clients[addr]  # Remove client from tracking
                continue

            # 📨 Send ACK for received packet
            server_socket.sendto(str(seq_num).encode(), addr)

        except ConnectionResetError:
            print("⚠️ A client disconnected forcefully.")
            continue
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

# Run the server in a separate thread
threading.Thread(target=handle_client, daemon=True).start()

while True:
    pass  # Keep the server running
