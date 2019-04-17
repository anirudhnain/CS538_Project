## Prereqs
- Python 3.6
- Solidity 4
- PySolc (Already in requirements.txt)
- geth (latest)
- RabbitMQ
- Pika (Already in requirements.txt)
## Setting up geth

https://medium.com/mercuryprotocol/how-to-create-your-own-private-ethereum-blockchain-dad6af82fc9f
Use "password" as your password to reduce code changes.

## To run geth
`geth --datadir ./myDataDir --networkid 1114 --rpcaddr "0.0.0.0" --rpccorsdomain "localhost" --rpc --rpcapi="db,eth,net,web3,personal,web3" console 2>> myEth.log`

## Setup Hyperledger Fabric 
https://hyperledger-fabric.readthedocs.io/en/release-1.4/getting_started.html

## Follow this to setup your blockchain network
https://hyperledger-fabric.readthedocs.io/en/release-1.4/write_first_app.html

## TODO
Figure out who writes the contract. How does the other party hear about it?
Advantages of API based system, data about speed.
