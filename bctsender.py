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
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
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

class Sender:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def mine_block(self, data):
        previous_block = self.blockchain.get_latest_block()
        new_block = Block(previous_block.index + 1, time.time(), data, previous_block.hash)
        self.blockchain.add_block(new_block)
        print(f"Block mined successfully with data: {data}")

    def send_blockchain(self, ip, port):
        blockchain_data = json.dumps([vars(block) for block in self.blockchain.chain])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(blockchain_data.encode())
        print(f"Blockchain sent successfully to {ip}:{port}")

# Example usage
blockchain = Blockchain()
sender = Sender(blockchain)

# Loop to allow user to add blocks
while True:
    user_data = input("Enter data for new block (or 'exit' to finish): ")
    if user_data.lower() == 'exit':
        break
    sender.mine_block(user_data)

# Send blockchain to receiver
receiver_ip = "127.0.0.1"  # Localhost for testing
receiver_port = 12345
sender.send_blockchain(receiver_ip, receiver_port)
