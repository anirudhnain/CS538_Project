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
    string public greeting;

    function Greeter() public {
        greeting = 'Hello';
    }

    function setGreeting(string _greeting) public {
        greeting = _greeting;
    }

    function greet() view public returns (string) {
        return greeting;
    }
}
'''
def get_channel(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
def get_greeter():
    return w3.eth.contract(
        address='',
        abi={},
    )
def blockchain_listener(contract_addr):
    channel = get_channel("blk_to_gateway")
    event_filter = w3.eth.filter({"address":contract_addr})
    while True:
        channel.basic_publish(exchange='',
                      routing_key='blk_to_gateway',
                      body=event_filter.get_new_entries())
        time.sleep(0.1)
def gateway_listener():
    def callback(ch, method, properties, body):
        #call smart contract function
        pass
    channel.basic_consume(queue='gateway_to_blk',
                      auto_ack=True,
                      on_message_callback=callback)
    channel.start_consuming()
if __name__ == '__main__':
    blk_to_gateway_channel()
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

    greeter.functions.setGreeting("Change").call()
    print(greeter.functions.greet().call())
    blockchain_listener = threading.Thread(target=blockchain_listener,args=("0x2d168915292c432147aa19e90971670879889220"))
    blockchain_listener.start()
    gateway_listener()