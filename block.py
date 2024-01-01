from hashlib import sha256
import time


class Block:

    def __init__(self, index, prev_hash, data):
        self.index = index 
        self.nonce = None 
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = time.time()
        self.hash = None
        self.merkle_tree_root = None
    @property
    def block_hash_calculation(self, difficulty=4):
        for nonce in range(10 ** 100):
            block_of_attributes = "{}{}{}{}".format(self.index, 
                                                    nonce, 
                                                    self.prev_hash, 
                                                    self.timestamp)
            hash = sha256(block_of_attributes.encode()).hexdigest()
            if hash.startswith(difficulty * '0'):
                self.hash = hash
                self.nonce = nonce
                break

    @property
    def merkle_tree_building(self):
        pass

    def info(self):
        print(f'index: {self.index}')
        print(f'nonce: {self.nonce}')
        print(f'hash: {self.hash}')
        print(f'merkle_tree_root: {self.merkle_tree_root}')
        print(f'timestamp: {self.timestamp}')
            