from hashlib import sha256
from copy import deepcopy
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
        trs = deepcopy(self.data)
        while len(trs) > 1:
            if len(trs) % 2 == 1:
                trs.append(trs[len(trs) - 1])
            for i in range(0, len(trs), 2):
                trs[i] = sha256(trs[i].encode()).hexdigest() + \
                sha256(trs[i + 1].encode()).hexdigest()
            trs = list(filter(lambda x: (x.index % 2 == 0), trs))
        self.merkle_tree_root = trs[0]
                
    def info(self):
        print(f'index: {self.index}')
        print(f'nonce: {self.nonce}')
        print(f'hash: {self.hash}')
        print(f'merkle_tree_root: {self.merkle_tree_root}')
        print(f'timestamp: {self.timestamp}')
            