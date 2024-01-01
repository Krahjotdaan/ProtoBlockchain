from blockchain import *


def main():
    blockchain = BlockChain()
    blockchain.construct_genesis()
    print("***Mining fccCoin about to start***")
    print(blockchain.blockchain)

    last_block = blockchain.last_block
    last_proof_no = last_block.nonce
    proof_no = blockchain.proof_of_work(last_proof_no)

    blockchain.new_transaction(
        sender="0",  #it implies that this node has created a new block
        recipient="Quincy Larson",  #let's send Quincy some coins!
        quantity=
        1,  #creating a new block (or identifying the proof number) is awarded with 1
    )

    block = blockchain.construct_block(proof_no, last_block.hash)

    print("***Mining fccCoin has been successful***")
    print(blockchain.blockchain)


if __name__ == '__main__':
    main()
    