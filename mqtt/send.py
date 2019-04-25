import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='gateway_to_blk')
channel.basic_publish(exchange='',
                      routing_key='gateway_to_blk',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()