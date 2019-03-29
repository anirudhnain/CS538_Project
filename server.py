from web3 import Web3
import web3.personal
from ens.auto import ns
import time
from solc import compile_source
from web3.contract import ConciseContract
w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
print(w3.eth.blockNumber)
# event_filter = w3.eth.filter({"address":Web3.toChecksumAddress("0x2d168915292c432147aa19e90971670879889220")})
# while True:
#     print(event_filter.get_new_entries())
#     time.sleep(1)
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
print('Default contract greeting: {}'.format(
    greeter.functions.greet().call()
))
greeter.functions.setGreeting("Ni Hao").call()
print(greeter.functions.greet().call())