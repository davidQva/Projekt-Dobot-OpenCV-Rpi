
import socket
import json
import time

def main():
    host = 'localhost'  # The server's hostname or IP address
    port = 12345        # The port used by the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"Connected to the server at {host}:{port}")

        # Sending "start" command
        client_socket.sendall("start".encode())
        response = client_socket.recv(1024).decode()
        print("Server response start:", response)

        while True:
            # Taking color inputs from the terminal
            colors = input("Enter the colors (separated by space): ").split()       
            # Sending an array of cubes with the input colors          
            client_socket.sendall(json.dumps(colors).encode())
            response = client_socket.recv(1024).decode()
            print("Server response:", response)

            # Sending "stop" command
            """  client_socket.sendall("stop".encode())
            response = client_socket.recv(1024).decode()
            print("Server response:", response) """

    finally:
        print("Closing connection to the server...")
        client_socket.close()

if __name__ == "__main__":
    main()
