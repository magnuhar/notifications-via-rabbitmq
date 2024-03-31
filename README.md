# RabbitMQ notifications

Simple little notifications stack that takes messages from RabbitMQ direct exchange and sends them either to phone (Pushover) or email (SendGrid).

To send a notification, post to the notifications exchange:

```py
import os
import dotenv
import pika

dotenv.load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASS")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(
            username=RABBITMQ_USERNAME,
            password=RABBITMQ_PASSWORD
        )
    )
)
channel = connection.channel()
channel.exchange_declare(exchange="notifications", exchange_type="direct")

# Send your notification to Pushover
channel.basic_publish(
    exchange="notifications",
    routing_key="phone",
    body=f'{{"body": "Hello World"}}'
)

# Send your notification via email
channel.basic_publish(
    exchange="notifications",
    routing_key="email",
    body=f'{{"recipient": "someemail@test.com", "subject": "Hello World", "body": "This is a test notification"}}'
)
```
