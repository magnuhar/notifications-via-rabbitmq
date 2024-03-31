# Notifications via RabbitMQ

Simple little notifications utility that takes messages from RabbitMQ direct exchange and sends them either to phone (Pushover) or email (SendGrid).

## Run

```
docker compose up
```

## Environment Variables

| Key | Description |
| --- | ----------- |
| **RABBITMQ** | https://www.rabbitmq.com/ |
| RABBITMQ_HOST | Address to the RabbitMQ host, e.g `localhost` |
| RABBITMQ_PORT | The port that RabbitMQ is running on, default `5672` |
| RABBITMQ_USER | The name of the user with which to connect to RabbitMQ |
| RABBITMQ_PASS | The password of the RabbitMQ user |
| **PUSHOVER** | https://pushover.net/ |
| PUSHOVER_API_KEY | The Pushover API key. Found in the control panel |
| PUSHOVER_USER_KEY | Your Pushover user key. Found in the control panel |
| **SENDGRID** | https://sendgrid.com/ |
| SENDGRID_API_KEY | SendGrid API key, created in SendGrid control panel |
| FROM_EMAIL | The email that is listed as sender. |

## Sending notifications

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
