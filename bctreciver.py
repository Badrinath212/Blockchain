import socket
import json
import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_info = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(block_info.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []

    def add_block(self, new_block):
        self.chain.append(new_block)

    def print_blockchain(self):
        print("Blockchain:")
        for block in self.chain:
            print(f"Block Number: {block.index}")
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(block.timestamp))}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print()

def start_receiver(ip, port):
    blockchain = Blockchain()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Server listening on {ip}:{port}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            buffer = b''
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                buffer += data
            blockchain_data = json.loads(buffer.decode())
            for block_data in blockchain_data:
                block = Block(
                    block_data['index'],
                    block_data['timestamp'],
                    block_data['data'],
                    block_data['previous_hash']
                )
                blockchain.add_block(block)
                # Print block information as it is added

            blockchain.print_blockchain()

# Example usage for receiver
receiver_ip = "127.0.0.1"  # Bind to localhost for testing
receiver_port = 12345
start_receiver(receiver_ip, receiver_port)
