import RPi.GPIO as GPIO
import time
import pika

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23,GPIO.OUT)
print "LED light is setup"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='blk_to_gateway')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    GPIO.output(23,GPIO.HIGH)
    time.sleep(1)
    print "LED off"
    GPIO.output(23,GPIO.LOW)

channel.basic_consume(queue='blk_to_gateway',
                      auto_ack=True,
                      on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()