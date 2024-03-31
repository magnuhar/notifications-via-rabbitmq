import json
import pika
import dotenv
import os
from common.connection import channel
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange="notifications", queue=queue_name, routing_key="email")

print("[*] Waiting for notifications. To exit press CTRL+C")

def send_email(recipient: str, subject: str, body: str):
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    from_email = os.getenv("FROM_EMAIL")
    to_email = recipient
    subject = subject
    content = Content("text/plain", body)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    print(response.status_code)

def callback(ch, method, properties, body: bytes):
    body = json.loads(body.decode("utf-8"))

    recipient = body["recipient"]
    subject = body["subject"]
    body = body["body"]

    send_email(recipient, subject, body)

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()