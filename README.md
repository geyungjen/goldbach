# Goldbach Distributed BigInt

This project demonstrates a distributed representation of integers using linked nodes over sockets and applies it to test Goldbach's Conjecture.

## Features

- Implements a `BigInt` class using a singly linked list for arbitrary-precision integers.
- Converts BigInts into distributed linked lists using networked node servers.
- Tests Goldbach's Conjecture using distributed computation for all even numbers up to a user-specified limit.

## How It Works

1. Each digit of a `BigInt` is stored in a node (least significant digit first).
2. These nodes are served by lightweight socket servers.
3. The `DistributedLinkedListClient` handles creating node servers, linking nodes, and retrieving data.
4. Goldbach's Conjecture is tested by finding two primes `p` and `q` such that `p + q = even_number`.
5. Each prime is converted into a `BigInt`, then distributed into networked nodes, and their contents are printed.

## Usage

```bash
python goldbach_tester.py --limit 50
```

Replace `50` with any even upper limit you wish to test.

## Modules

- `goldbach_tester.py`: Main script with BigInt integration and entry point.
- `BigInt`: Internal linked-list-based integer class with add, subtract, multiply, and comparison operations.
- `DistributedLinkedListClient`: Creates and traverses the distributed node network.
- `distributed_node_server.py`: Hosts each digit as a node server.
- `node_client_util.py`: Utility to set `next_node` and get node data.

## Dependencies

- Python 3.8+
- `multiprocessing`, `socket`, `json`, `argparse`

## License

MIT License
