'use strict';
/*
 * The light provider server connects to the hyperledger fabric as well as the Rabbit MQTT broker
 */

var amqp = require('amqplib/callback_api');

amqp.connect('amqp://localhost', function(connErr, connection) {
    if (connErr) {
        throw connErr;
    }
    connection.createChannel(function(chErr, channel) {
        if (chErr) {
            throw chErr;
        }

        var queue = 'blk_to_gateway';

        channel.assertQueue(queue, {durable: false});

        console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

        channel.consume(queue, function(msg) {
            console.log(" [x] Received %s", msg.content.toString());
        }, {
            noAck: true
        });
    });
});




/*
const { FileSystemWallet, Gateway } = require('fabric-network');
const fs = require('fs');
const path = require('path');

const ccpPath = path.resolve(__dirname, '..', '..', 'basic-network', 'connection.json');
const ccpJSON = fs.readFileSync(ccpPath, 'utf8');
const ccp = JSON.parse(ccpJSON);

async function main() {
    try {

        // Create a new file system based wallet for managing identities.
        const walletPath = path.join(process.cwd(), 'wallet');
        const wallet = new FileSystemWallet(walletPath);
        console.log(`Wallet path: ${walletPath}`);

        // Check to see if we've already enrolled the user.
        const userExists = await wallet.exists('user1');
        if (!userExists) {
            console.log('An identity for the user "user1" does not exist in the wallet');
            console.log('Run the registerUser.js application before retrying');
            return;
        }

        // Create a new gateway for connecting to our peer node.
        const gateway = new Gateway();
        await gateway.connect(ccp, { wallet, identity: 'user1', discovery: { enabled: false } });

        // Get the network (channel) our contract is deployed to.
        const network = await gateway.getNetwork('mychannel');

        // Get the contract from the network.
        const contract = network.getContract('greeter1');

        // Evaluate the specified transaction.
        // queryCar transaction - requires 1 argument, ex: ('queryCar', 'CAR4')
        // queryAllCars transaction - requires no arguments, ex: ('queryAllCars')
        const result = await contract.evaluateTransaction('queryGreet');
        console.log(`Transaction has been evaluated, result is: ${result.toString()}`);

        await contract.submitTransaction('toggleGreet');

        const result = await contract.evaluateTransaction('queryGreet');
        console.log(`Transaction has been evaluated, result is: ${result.toString()}`);

        console.log('All transactions are completed');
    } catch (error) {
        console.error(`Failed to evaluate transaction: ${error}`);
        process.exit(1);
    }
}

main();*/
