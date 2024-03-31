import pika
import sys
from connection import channel


subject = "Test Message"
body = "This is a test message"
recipient = "CHANGEME@test.com"

channel.basic_publish(
    exchange="notifications",
    routing_key="email",
    body=f'{{"recipient": "{recipient}", "subject": "{subject}", "body": "{body}"}}'
)

print(f" [x] Sent '{subject}' to '{recipient}'")