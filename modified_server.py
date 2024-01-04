
import socket
import json


class Observer:
    def update(self, message):
       raise NotImplementedError("Subclass must implement abstract method")

class Server:   
    
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.observers = []
       

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        self.conn, self.addr = self.server_socket.accept()
        print(f"Accepted connection from {self.addr}")
        self.handle_client()

    def register_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)       
        
    def handle_client(self):        
        global start
        start = False
        try:
            while True:
                data = self.conn.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                if message == "start" or message == "stop":
                    start = True if message == "start" else False
                    self.notify_observers(message)
                    self.conn.sendall("done".encode())                    
                else:
                    try:
                        cubes = json.loads(message)
                        if isinstance(cubes, list) and len(cubes) <= 5:
                            self.notify_observers(cubes)
                            self.conn.sendall("done".encode())                          
                        else:
                            self.conn.sendall("error".encode())
                    except json.JSONDecodeError:
                        self.conn.sendall("error".encode())
        finally:
            self.conn.close()         

    def stop(self):
        self.server_socket.close()
 
class MessageLogger(Observer):
    def update(self, message):
        print(f"Message from server: {message}")

# Example usage
if __name__ == "__main__":

    server = Server()
    server.register_observer(MessageLogger())
    server.start()
