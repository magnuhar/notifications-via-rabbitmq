import json
from common.connection import channel
import httpx
import dotenv
import os

dotenv.load_dotenv()

PUSHOVER_API_KEY = os.getenv("PUSHOVER_API_KEY")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")

result = channel.queue_declare(queue="", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange="notifications", queue=queue_name, routing_key="phone")

print("[*] Waiting for notifications. To exit press CTRL+C")

def callback(ch, method, properties, body: bytes):
    print(f" [x] Received {body.decode('utf-8')}")

    json_body = json.loads(body.decode("utf-8"))

    body = json_body["body"]

    print(f" [x] Sending '{body}' to Pushover")

    httpx.post(
        url="https://api.pushover.net/1/messages.json",
        data={
            "token": PUSHOVER_API_KEY,
            "user": PUSHOVER_USER_KEY,
            "message": body,
        },
    )

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()