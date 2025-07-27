# distributed_node_server.py

import socketserver
import json
from distributed_node import DistributedNode

class DistributedNodeServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(self, server_address, node_instance):
        self.node_instance = node_instance
        super().__init__(server_address, self.Handler)

    class Handler(socketserver.BaseRequestHandler):
        def handle(self):
            try:
                data = self.request.recv(1024).decode()
                request = json.loads(data)

                if request["type"] == "get_node_info":
                    response = {
                        "node_info": self.server.node_instance.to_dict()
                    }

                elif request["type"] == "update_next_node":
                    self.server.node_instance.next_node_address = request["next_node_address"]
                    response = {"status": "ok"}

                else:
                    response = {"error": "Unknown request type"}

            except Exception as e:
                response = {"error": str(e)}

            self.request.sendall(json.dumps(response).encode())

