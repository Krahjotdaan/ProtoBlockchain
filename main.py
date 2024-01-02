from blockchain import *


def main():
    blockchain = BlockChain()
    blockchain.construct_genesis()
    print("Start of mining")
    print(blockchain.blockchain)

    last_block = blockchain.last_block
    last_nonce = last_block.nonce
    nonce = blockchain.proof_of_work(last_nonce)

    blockchain.new_transaction(
        sender="0", 
        recipient="Quincy Larson",  
        quantity=1,  
    )

    block = blockchain.construct_block(nonce, last_block.hash)

    print("***Mining was successful***")
    print(blockchain.blockchain)


if __name__ == '__main__':
    main()
    