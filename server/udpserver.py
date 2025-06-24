import socket
import time

def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("0.0.0.0", 5555))  
    print("🔵 UDP Server is listening on port 5555...\n")

    expected_seq = 1  # Expected sequence number
    client_addr = None
    session_start_time = None  # Track total session duration

    while True:
        data, addr = server_socket.recvfrom(1024)
        recv_time = time.time()  # Timestamp when the packet arrives

        # If first connection, log the connection establishment
        if client_addr is None:
            client_addr = addr
            session_start_time = recv_time  # Mark the start time
            print(f"✅ Connection established with {addr}\n")

        # Extract sequence number, send time, and message
        try:
            parts = data.decode().split(":")
            seq_num = int(parts[0])
            send_time = float(parts[1])
            message = ":".join(parts[2:])
        except (ValueError, IndexError):
            print("⚠️ Received malformed packet!")
            continue

        # Detect packet loss
        if seq_num != expected_seq:
            dropped = seq_num - expected_seq
            print(f"⚠️ Packet Drop Detected! Expected {expected_seq}, but received {seq_num} (Dropped {dropped} packet(s))")

        expected_seq = seq_num + 1  # Update expected sequence number

        # Calculate delay for the current packet
        delay = recv_time - send_time
        print(f"📩 Received Packet {seq_num} from {addr} | Delay: {delay:.4f} sec | Message: '{message}'")

        # If the client sends "exit", show the total session duration and close
        if message.lower() == "exit":
            total_session_time = time.time() - session_start_time
            print(f"\n🔴 Client {addr} disconnected. Total Session Duration: {total_session_time:.4f} sec\n")
            client_addr = None  # Reset for new connections

if __name__ == "__main__":
    udp_server()
