import socket
import time
import os

def client_program():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Ask the user whether to use a wired or wireless connection
    connection_type = input("Do you want to use a wired or wireless connection? (wired/wireless): ").strip().lower()
    
    if connection_type == "wired":
        # Assuming the wired interface uses a specific IP or network configuration
        # Check if Ethernet cable is available or not
        ethernet_connected = os.system("ping -c 1 google.com") == 0  # Basic check for network connection

        if not ethernet_connected:
            print("You cannot use wired transmission as Ethernet cable is not connected.")
            print("Please connect an Ethernet cable to your device for wired transmission.")
            return  # Exit the program as wired transmission cannot proceed without Ethernet

        server_address = input("Enter server IP (default: 127.0.0.1): ") or "127.0.0.1"
    
    elif connection_type == "wireless":
        # Assuming the wireless interface uses a specific IP or network configuration
        server_address = input("Enter server IP (default: 127.0.0.1): ") or "127.0.0.1"
    else:
        print("Invalid choice. Defaulting to wired connection.")
        server_address = "127.0.0.1"
    
    server_port = 5555
    client.connect((server_address, server_port))
    print(f"Connected to the server at {server_address} via {connection_type} connection!")

    while True:
        message = input("Enter message (type 'exit' to disconnect, 'SEND_FILE <filename>' to send a file): ")

        if message.lower() == 'exit':
            print("Disconnecting...")
            client.close()
            break

        elif message.startswith("SEND_FILE"):
            try:
                _, file_name = message.split()
                client.send(message.encode())

                # Record the start time for file transmission
                start_time = time.time()

                with open(file_name, "rb") as f:
                    while chunk := f.read(1024):
                        client.send(chunk)

                client.send(b"END_FILE")

                # Measure time for file transmission
                end_time = time.time()
                print(f"File '{file_name}' sent. Transmission delay: {end_time - start_time:.4f} seconds")

            except FileNotFoundError:
                print(f"File '{file_name}' not found.")
        
        else:
            # Record the start time for message round-trip time calculation
            start_time = time.time()

            client.send(message.encode())
            response = client.recv(1024).decode()

            # Measure round-trip time
            end_time = time.time()
            print(f"Server: {response}")
            print(f"Round-trip time: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    client_program()
