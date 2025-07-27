import socket
import pickle

def get_node_data(address):
    host, port = address.split(":")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, int(port)))
        s.sendall(b"get_data")
        data = s.recv(1024)
        return pickle.loads(data)

def set_next_node(address, next_address):
    host, port = address.split(":")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, int(port)))
        command = f"set_next:{next_address}"
        s.sendall(command.encode())
        return s.recv(1024).decode()

def shutdown_node(address):
    host, port = address.split(":")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, int(port)))
        s.sendall(b"shutdown")
        return s.recv(1024).decode()
