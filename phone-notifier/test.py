import pika
import sys
from connection import channel


channel.basic_publish(
    exchange="notifications",
    routing_key="phone",
    body=f'{{"body": "This is a test message from phone-notifier"}}'
)