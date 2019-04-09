from web3 import Web3
import web3.personal
from ens.auto import ns
import time
from solc import compile_source
from web3.contract import ConciseContract
import threading
import pika
#try to read contract address from db
#if not found mine contract and store in db
#start listening for events

#on transaction init from gateway send transaction to blockchain



# Solidity source code
contract_source_code = '''
pragma solidity ^0.4.21;

contract Greeter {
    event Greet(
        bool greeting
    );
    bool public greeting;

    function Greeter() public {
        greeting = false;
    }

    function toggleGreeting() public {
        greeting = !greeting;
        emit Greet(greeting);
    }

    function greet() view public returns (bool) {
        return greeting;
    }
}
'''
def get_channel(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    return channel
def get_greeter():
    return None
    # return w3.eth.contract(
    #     address='',
    #     abi={},
    # )
def blockchain_listener(contract_addr,greeter):
    channel = get_channel("blk_to_gateway")
    event_filter = greeter.events.Greet.createFilter(fromBlock='latest')
    while True:
        entries = event_filter.get_new_entries()
        
        if not len(entries) == 0:
            channel.basic_publish(exchange='', routing_key='blk_to_gateway',body=str(greeter.functions.greet().call()))
        time.sleep(1)

def gateway_listener(greeter):
    channel = get_channel('gateway_to_blk')
    callback = lambda ch, method, properties, body: greeter.functions.toggleGreeting().transact()
    channel.basic_consume(queue='gateway_to_blk',
                      auto_ack=True,
                      on_message_callback=callback)
    channel.start_consuming()
if __name__ == '__main__':
    #blk_to_gateway_channel()
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    greeter = get_greeter()
    if greeter == None:
        compiled_sol = compile_source(contract_source_code) # Compiled source code
        contract_interface = compiled_sol['<stdin>:Greeter']
        w3.eth.defaultAccount = w3.eth.accounts[0]
        personal = web3.personal.Personal(w3)
        personal.unlockAccount(w3.eth.accounts[0],"password")
        Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        tx_hash = Greeter.constructor().transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        greeter = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_interface['abi'],
        )

    print(greeter,greeter.address,greeter.abi)
    # tx_hash = greeter.functions.toggleGreeting().transact()
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print("State",greeter.functions.greet().call())
    # print(w3.eth.getTransaction(tx_receipt.transactionHash.hex()))
    # tx_hash = greeter.functions.toggleGreeting().transact()
    # tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    # print("State",greeter.functions.greet().call())
    # print(w3.eth.getTransaction(tx_receipt.transactionHash.hex()))
    # print("><>>>>>>>>>>",tx_receipt)
    blockchain_listener = threading.Thread(target=blockchain_listener,args=(greeter.address,greeter))
    blockchain_listener.start()
    gateway_listener(greeter)