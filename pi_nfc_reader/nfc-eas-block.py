"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""
import sys
sys.path.insert(0, './../ethereum/')
import board
import busio
import time

from digitalio import DigitalInOut
from adafruit_pn532.spi import PN532_SPI
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from latency import openTimeLogFile, logTime, closeFile

def main():
	logFile = openTimeLogFile('nfc_reader_log.txt')
	pn532 = initSPI()	
	mqttClient = initmqtt()
	
	mqttClient.subscribe('onPayment/1', 1, onPayment)

	print('Waiting for RFID/NFC card...')
	while True:
		# Check if a card is available to read
		uid = pn532.read_passive_target(timeout=0.5)
		# Try again if no card is available.
		if uid is None:
			continue
		print('Found card with UID:', [hex(i) for i in uid])
		productId = readProductId(pn532)
		#if productId is not None:
		#print('Data:', [chr(x) for x in productId])
		logTime(logFile,"nfcReaderPublished")
		mqttClient.publish('onPayment/1', 'Product Data',1)
		#time.sleep(2)

		time.sleep(1)

	

def initSPI():
	# SPI connection:
	spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
	cs_pin = DigitalInOut(board.D5)
	pn532 = PN532_SPI(spi, cs_pin, debug=False)
	ic, ver, rev, support = pn532.get_firmware_version()
	print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
	# Configure PN532 to communicate with MiFare cards
	pn532.SAM_configuration()
	return pn532


def initmqtt():
	# For certificate based connection
	print('Initializing MQTT client')	
	mqttClient = AWSIoTMQTTClient("nfc_eas_pi")
	mqttClient.configureEndpoint("a389804w7ex2ae-ats.iot.us-east-2.amazonaws.com", 8883)
	mqttClient.configureCredentials("./certs/aws-iot-root-ca1.pem", "./certs/12ccd5737a-private.pem.key", "./certs/12ccd5737a-certificate.pem.crt")
	mqttClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
	mqttClient.configureDrainingFrequency(2)  # Draining: 2 Hz
	mqttClient.configureConnectDisconnectTimeout(10)  # 10 sec
	mqttClient.configureMQTTOperationTimeout(5)  # 5 sec
	mqttClient.connect()
	print('MQTT client initialized and connected')
	return mqttClient


def readProductId(pn532):	
	productId = bytearray(b'')
	
	try:	
		for x in range(0,3):
			productId = productId + pn532.ntag2xx_read_block(7+x)
	except TypeError:
		print('Error while reading the NFC tag. Please try again')
		productId = None
			
	return productId	

def onPayment(client, userdata, message):
	print(message.topic)
	print(message.payload)


	
if __name__=="__main__":
	main()

