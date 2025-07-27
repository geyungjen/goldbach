import multiprocessing
import socket
import json
import time
import sys

from distributed_node import DistributedNode
from distributed_node_server import DistributedNodeServer

class DistributedLinkedListClient:
    def __init__(self, address=None):
        self.head_node_address = address

    def traverse(self):
        current_address = self.head_node_address
        while current_address:
            node = self.get_node_info(current_address)
            if node:
                print(f"Node Data: {node.data}")
                current_address = node.next_node_address
            else:
                break

    def get_node_info(self, node_address):
        try:
            if isinstance(node_address, tuple):
               if len(node_address) == 2:
                   host, port = node_address
               else:
                   node_address=list(node_address)
                   node_address=''.join(node_address) 
                   host, port = node_address.split(":")
#                   print(node_address)
            else:
                host, port = node_address.split(":")
#                print(node_address)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, int(port)))
                request = {"type": "get_node_info"}
                sock.sendall(json.dumps(request).encode())
                response_data = sock.recv(1024).decode()
                response = json.loads(response_data)
                if "node_info" in response:
                    return DistributedNode.from_dict(response["node_info"])
                else:
                    print(f"Error getting node info: {response.get('error')}")
                    return None
        except Exception as e:
            print(f"Error connecting to node at {node_address}: {e}")
            return None

    def set_next_node(self, from_address, to_address):
        host, port = from_address.split(":")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, int(port)))
            request = {
                "type": "update_next_node",
                "next_node_address": to_address
            }
            sock.sendall(json.dumps(request).encode())

    def build_distributed_list(self, digits):
        addresses = []
        for d in digits:
            addr, _ = self.create_node_server(int(d))
            addresses.append(addr)

        # link the nodes
        for i in range(len(addresses) - 1):
            self.set_next_node(addresses[i], addresses[i + 1])

        return DistributedLinkedListClient(addresses[0])  # return client with head

    def create_node_server(self, data):
        node = DistributedNode(data)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 0))
            host, port = s.getsockname()

        def run_server():
            with DistributedNodeServer(('localhost', port), node) as server:
                server.serve_forever()

        process = multiprocessing.Process(target=run_server, daemon=True)
        process.start()

        time.sleep(0.1)  # give time for the server to start

        return (f'localhost:{port}', node)

