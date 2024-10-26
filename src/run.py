import json
import pika, os
from generators.tech_news import TechNewsGenerator
from dotenv import load_dotenv
from rich import print

print(f'Load .env: {load_dotenv(dotenv_path="./resources/.env")}', flush=True)

url = os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672/%2f")


def process_message(ch, method, properties, body):
    urls = json.loads(body.decode("utf-8")).get("urls")  # Get the URLs from the message
    # Here you would process the URLs and generate the response
    generator = TechNewsGenerator(llm="gemini-1.5-pro")
    # Act
    result = generator.generate(
        length=3000,
        references=urls,
    )
    # Send the response back to the queue
    response_queue = "response_queue"
    ch.basic_publish(
        exchange="", routing_key=response_queue, body=result.encode("utf-8")
    )


connection = pika.BlockingConnection(pika.URLParameters(url))
channel = connection.channel()
channel.queue_declare(queue="task_queue", durable=True)
channel.queue_declare(queue="response_queue", durable=True)

channel.basic_consume(
    queue="task_queue", on_message_callback=process_message, auto_ack=True
)

print(" [*] Waiting for messages.")
channel.start_consuming()
