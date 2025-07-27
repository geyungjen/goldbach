import argparse
import platform
from distributed_linked_list_client import DistributedLinkedListClient
from node_client_util import get_node_data, set_next_node

# Node class for BigInt internal linked list
class Node:
    def __init__(self, digit: int):
        self.digit = digit  # digit must be 0-9
        self.next = None

# Arbitrary-precision integer class using singly linked list
class BigInt:
    def __init__(self, number: str):
        # Store digits in reverse order for easier math: 123 -> 3 -> 2 -> 1
        self.head = None
        for ch in reversed(number.strip()):
            if not ch.isdigit():
                raise ValueError("Invalid digit in number")
            new_node = Node(int(ch))
            new_node.next = self.head
            self.head = new_node

    @staticmethod
    def from_int(n: int):
        return BigInt(str(n))

    def __str__(self):
        # Convert linked list to string representation of the number
        digits = []
        current = self.head
        while current:
            digits.append(str(current.digit))
            current = current.next
        return ''.join(reversed(digits))

    def to_digits(self):
        # Convert linked list to a list of digits
        digits = []
        current = self.head
        while current:
            digits.append(current.digit)
            current = current.next
        return digits

    def add(self, other):
        # Add two BigInt numbers
        p1, p2 = self.head, other.head
        carry = 0
        dummy_head = Node(0)
        current = dummy_head

        while p1 or p2 or carry:
            sum_val = carry
            if p1:
                sum_val += p1.digit
                p1 = p1.next
            if p2:
                sum_val += p2.digit
                p2 = p2.next
            carry = sum_val // 10
            current.next = Node(sum_val % 10)
            current = current.next

        result = BigInt("0")
        result.head = dummy_head.next
        return result

    def subtract(self, other):
        # Subtract one BigInt from another (assumes self >= other)
        p1, p2 = self.head, other.head
        dummy_head = Node(0)
        current = dummy_head
        borrow = 0

        while p1:
            diff = p1.digit - (p2.digit if p2 else 0) - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            current.next = Node(diff)
            current = current.next
            p1 = p1.next
            if p2:
                p2 = p2.next

        result = BigInt("0")
        result.head = dummy_head.next
        return result

    def compare(self, other):
        # Compare two BigInts: -1 if self < other, 0 if equal, 1 if self > other
        def reverse_list(head):
            prev = None
            while head:
                next_node = head.next
                head.next = prev
                prev = head
                head = next_node
            return prev

        a = reverse_list(self.head)
        b = reverse_list(other.head)

        pa, pb = a, b
        while pa and pb:
            if pa.digit > pb.digit:
                return 1
            elif pa.digit < pb.digit:
                return -1
            pa = pa.next
            pb = pb.next

        if pa: return 1
        if pb: return -1
        return 0

    def __eq__(self, other):
        return self.compare(other) == 0

    def __lt__(self, other):
        return self.compare(other) == -1

    def __gt__(self, other):
        return self.compare(other) == 1

    @staticmethod
    def two_based_exp(m):
        # Compute 2^m as a BigInt
        result = BigInt("1")
        for _ in range(m):
            result = result.multiply_by_two()
        return result

    def multiply_by_two(self):
        # Multiply BigInt by 2
        current = self.head
        carry = 0
        dummy_head = Node(0)
        result_current = dummy_head

        while current or carry:
            product = (current.digit if current else 0) * 2 + carry
            carry = product // 10
            result_current.next = Node(product % 10)
            result_current = result_current.next
            if current:
                current = current.next

        result = BigInt("0")
        result.head = dummy_head.next
        return result

    def to_distributed(self, client_class):
        # Convert BigInt to a distributed linked list
        client = client_class()
        digits = self.to_digits()
        return client.build_distributed_list(digits)

    @staticmethod
    def from_distributed(client, head_address):
        # Convert from distributed linked list back to BigInt
        digits = []
        current_address = head_address
        while current_address:
            node = client.get_node_info(current_address)
            if node:
                digits.append(str(node.data))
                current_address = node.next_node_address
            else:
                break
        number_str = ''.join(reversed(digits))
        return BigInt(number_str)

# Function to test Goldbach's conjecture using distributed BigInts
def goldbach_test(limit=20):
    print(f"Testing Goldbach's Conjecture with DistributedBigInt up to {limit}:")
    for even in range(4, limit + 1, 2):
        found = False
        for p in range(2, even):
            q = even - p
            if is_prime(p) and is_prime(q):
                # Convert p and q into distributed BigInts and print them
                big_p = BigInt.from_int(p).to_distributed(DistributedLinkedListClient)
                big_q = BigInt.from_int(q).to_distributed(DistributedLinkedListClient)
                print(f"{even} = {p} + {q} → Distributed:")
                print("P:")
                big_p.traverse()
                print("Q:")
                big_q.traverse()
                found = True
                break
        if not found:
            print(f"Failed to find prime pair for {even}")

# Check if a number is prime (naive test)
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def is_linux():
    """
    Checks if the current operating system is Linux.
    Returns True if it's Linux, False otherwise.
    """
    return platform.system() == "Linux"

# Main entry point with command-line argument support
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Goldbach's Conjecture with Distributed BigInts")
    parser.add_argument("--limit", type=int, default=20, help="Upper bound of even numbers to test")
    args = parser.parse_args()

    # Linux-only runtime check due to multiprocessing fork limitations
    if not is_linux():
        print("This program requires Linux due to reliance on multiprocessing with fork().")
        exit(1)

    print("Testing Goldbach Distributed BigInt")
    goldbach_test(args.limit)
    print("Goldbach test finished")

