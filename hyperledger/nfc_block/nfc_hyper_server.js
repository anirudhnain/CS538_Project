'use strict';
// The NFC reader server connects to the hyperledger fabric as well as to the AWS broker
var awsIot = require('aws-iot-device-sdk');

var device = awsIot.device({
    keyPath: './certs/7e9203e1cc-private.pem.key',
    certPath: './certs/7e9203e1cc-certificate.pem.crt',
    caPath: './certs/AmazonRootCA1.pem',
    clientId: 'nfc_block_client_hyper',
    host: 'a389804w7ex2ae-ats.iot.us-east-2.amazonaws.com'
});

//
// Device is an instance returned by mqtt.Client(), see mqtt.js for full
// documentation.
//
device.on('connect', function() {
        console.log('connect');
        device.subscribe('onPayment/1');
        device.publish('onPayment/1', JSON.stringify({ test_data: 1}));
    });

device.on('message', function(topic, payload) {
        console.log('message', topic, payload.toString());
    });