#!venv/bin/python3

import pika
import sys
import os

def main():
    exchange_name = input('Enter Exchange Name:')

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    queue_name = 'Trace' + exchange_name
    routing_key = 'publish.' + exchange_name

    channel.queue_declare(queue_name)
    channel.queue_bind(queue_name, 'amq.rabbitmq.trace', routing_key)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        print("      Channel %r" % ch)
        print("      Method %r" % method)
        print("      Properties %r" % properties)

    channel.basic_consume(queue=queue_name,
                          auto_ack=True,
                          on_message_callback=callback)

    print('[*] Waiting for messages. Press CTRL+C to exit.')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
