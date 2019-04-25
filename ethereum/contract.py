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

def get_contract(w3):
    #return None
     return w3.eth.contract(
         address='0xCC806e9243C3B2c2Cc10CD4dFf45176203bA2369',
         abi=[{'constant': False, 'inputs': [], 'name': 'toggleGreeting', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'greet', 'outputs': [{'name': '', 'type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'greeting', 'outputs': [{'name': '','type': 'bool'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'anonymous': False, 'inputs': [{'indexed': False, 'name': 'greeting', 'type': 'bool'}], 'name': 'Greet', 'type': 'event'}]
     )
