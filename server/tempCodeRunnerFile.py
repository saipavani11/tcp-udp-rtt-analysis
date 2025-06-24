import socket
import threading
import time

def handle_client(client_socket, client_id):
    while True:
        try:
            start_time = time.time()  # Record the time when the server starts receiving data
            
            data = client_socket.recv(1024)
            if not data:
                print(f"Client {client_id} disconnected.")
                break
            
            message = data.decode()

            if message.startswith("SEND_FILE"):
                _, file_name = message.split()
                print(f"Receiving file '{file_name}' from Client {client_id}...")
                with open(f"{client_id}_{file_name}", "wb") as f:
                    while True:
                        chunk = client_socket.recv(1024)
                        if chunk.endswith(b"END_FILE"):
                            f.write(chunk[:-8])  # Write data except END_FILE
                            break
                        f.write(chunk)
                
                print(f"File '{file_name}' received from Client {client_id}.")
            else:
                print(f"Client {client_id}: {message}")
                client_socket.send(f"Message received: {message}".encode())

            # Calculate the end-to-end delay for the message processing
            end_time = time.time()
            total_delay = end_time - start_time
            print(f"Total delay for Client {client_id}: {total_delay:.4f} ms")
        
        except Exception as e:
            print(f"Error with Client {client_id}: {e}")
            break

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("192.168.204.58", 5555))
    server.listen(5)
    print("Server is listening on port 5555...")
    client_id = 0

    while True:
        client_socket, addr = server.accept()
        client_id += 1
        print(f"Client {client_id} connected from {addr}.")
        thread = threading.Thread(target=handle_client, args=(client_socket, client_id))
        thread.start()

if __name__ == "__main__":
    main()
