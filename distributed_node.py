# distributed_node.py

class DistributedNode:
    def __init__(self, data, next_node_address=None):
        self.data = data
        self.next_node_address = next_node_address

    def to_dict(self):
        return {
            "data": self.data,
            "next_node_address": list(self.next_node_address) if self.next_node_address else None
    }


    @staticmethod
    def from_dict(d):
        return DistributedNode(
            d["data"],
            tuple(d["next_node_address"]) if d["next_node_address"] else None
        )


