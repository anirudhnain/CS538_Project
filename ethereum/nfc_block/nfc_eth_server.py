# Import SDK packages
import sys
sys.path.insert(0, './../')
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from contract import contract_source_code, get_contract
from web3 import Web3
import web3.personal
from solc import compile_source
from time import sleep
from latency import openTimeLogFile, logTime, closeFile

contract = None
logFile = openTimeLogFile('nfc_block_server_log.txt')

def initMqttClient():
    myMQTTClient = AWSIoTMQTTClient("nfc_block_client")
    myMQTTClient.configureEndpoint("a389804w7ex2ae-ats.iot.us-east-2.amazonaws.com", 8883)
    myMQTTClient.configureCredentials("./certs/AmazonRootCA1.pem", "./certs/ac46a0e942-private.pem.key", "./certs/ac46a0e942-certificate.pem.crt")

    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    myMQTTClient.connect()
    print("Connection to MQTT broker successfully established")
    return myMQTTClient


def initContract(w3):
    print("Initializing contract",flush=True)
    greeter = get_contract(w3)
    w3.eth.defaultAccount = w3.eth.accounts[0]
    personal = web3.personal.Personal(w3)
    personal.unlockAccount(w3.eth.accounts[0],"password")
    if greeter == None:
        print("No contract. Creating new greeter contract",flush=True)
        compiled_sol = compile_source(contract_source_code) # Compiled source code
        contract_interface = compiled_sol['<stdin>:Greeter']
        Greeter = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        tx_hash = Greeter.constructor().transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        greeter = w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=contract_interface['abi'],
        )
    return greeter


def onScanCallBack(client, userdata, message):
    print("Received a mqtt message",flush=True)
    print("contract:",contract, flush=True)
    if contract is not None:
        print("Transacting with the contract",flush=True)
        contract.functions.toggleGreeting().transact()
        logTime(logFile,"publishedTxToBlockchain")
        print("Successfully state changed inside the contract",flush=True)


if __name__ == '__main__':
    print("Starting nfc ethereum server\n", flush=True)
    mqttClient =  initMqttClient()
    w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    contract = initContract(w3)
    print(contract,contract.address,contract.abi)
    mqttClient.subscribe("onPayment/1", 1, onScanCallBack)
    print("Listening for msgs from scanner\n",flush=True)
    while True:
        sleep(5)
    closeFile(logFile)