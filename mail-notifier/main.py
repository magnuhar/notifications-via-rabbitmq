import json
import pika
import dotenv
import os
from sg import send_email
from connection import channel

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange="notifications", queue=queue_name, routing_key="email")

print("[*] Waiting for notifications. To exit press CTRL+C")

def callback(ch, method, properties, body: bytes):
    body = json.loads(body.decode("utf-8"))

    recipient = body["recipient"]
    subject = body["subject"]
    body = body["body"]

    send_email(recipient, subject, body)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()