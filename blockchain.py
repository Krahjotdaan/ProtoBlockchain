from hashlib import sha256
from copy import deepcopy
import time


class Block:

    def __init__(self, index, nonce, prev_hash, data):
        self.index = index 
        self.nonce = nonce 
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = time.time()
        self.hash = None
        self.merkle_tree_root = None

    @property
    def block_hash_calculation(self):
            block_of_attributes = "{}{}{}{}".format(self.index, 
                                                    self.nonce, 
                                                    self.prev_hash, 
                                                    self.timestamp)
            self.hash = sha256(block_of_attributes.encode()).hexdigest()

    @property
    def merkle_tree_building(self):
        try:
            trs = deepcopy(self.data)
            for i in range(len(trs)):
                trs[i] = ''.join((trs[i]['sender'], 
                             trs[i]['recipient'], 
                             str(trs[i]['quantity'])),)
            if len(trs) % 2 == 1:
                trs.append(trs[-1])    
            while len(trs) > 1:
                for i in range(0, len(trs), 2):
                    trs[i] = sha256(trs[i].encode()).hexdigest() + \
                    sha256(trs[i + 1].encode()).hexdigest()
                    trs[i] = sha256(trs[i].encode()).hexdigest()
                del trs[1::2]
            self.merkle_tree_root = trs[0]
        except IndexError:
            self.merkle_tree_root = None

    @staticmethod
    def validation(block, prev_block):
        if prev_block.index + 1 != block.index:
            return False
        elif prev_block.calculate_hash != block.prev_hash:
            return False
        elif not BlockChain.verifying_proof(block.proof_no,
                                            prev_block.proof_no):
            return False
        elif block.timestamp <= prev_block.timestamp:
            return False

        return True

    def __repr__(self):
        return "{} - {} - {} - {} - {} - {}".format(
                                                self.index, 
                                                self.nonce,
                                                self.hash,
                                                self.prev_hash, 
                                                self.merkle_tree_root,
                                                self.timestamp)
                
    def info(self):
        print(f'index: {self.index}')
        print(f'nonce: {self.nonce}')
        print(f'hash: {self.hash}')
        print(f'merkle_tree_root: {self.merkle_tree_root}')
        print(f'timestamp: {self.timestamp}')
            

class BlockChain:

    def __init__(self):
        self.blockchain = []
        self.current_data = []
        self.nodes = set()

    def construct_genesis(self):
        self.construct_block(nonce=0, prev_hash='0000000000000000000000000000000000000000000000000000000000000000')
    
    def construct_block(self, nonce, prev_hash):
        block = Block(len(self.blockchain), nonce, prev_hash, self.current_data)
        self.current_data = []
        block.block_hash_calculation
        block.merkle_tree_building
        self.blockchain.append(block)

        return block
    
    def new_transaction(self, sender, recipient, quantity):
        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity
        })
    
    @staticmethod
    def proof_of_work(last_nonce):
        nonce = 0
        while not BlockChain.verifying_proof(nonce, last_nonce):
            nonce += 1

        return nonce
    
    @staticmethod
    def verifying_proof(last_nonce, nonce):
        guess_hash = sha256(f'{last_nonce}{nonce}'.encode()).hexdigest()
        return guess_hash[:4] == "0000"
    
    @property
    def last_block(self):
        return self.blockchain[-1]
    
    def block_mining(self, details_miner):
        self.new_transaction(
            sender="0",
            receiver=details_miner,
            quantity=1, 
        )

        last_block = self.last_block

        last_nonce = last_block.nonce
        nonce = self.proof_of_work(last_nonce)

        last_hash = last_block.calculate_hash
        block = self.construct_block(nonce, last_hash)

        return vars(block)
    
    def create_node(self, address):
        self.nodes.add(address)
