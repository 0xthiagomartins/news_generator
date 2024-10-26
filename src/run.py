import json
import os
from dotenv import load_dotenv
from rich import print
from nameko.standalone.rpc import ClusterRpcProxy

# Load environment variables
load_dotenv(dotenv_path="./resources/.env")

CONFIG = {
    "AMQP_URI": os.environ.get("CLOUDAMQP_URL", "amqp://guest:guest@localhost:5672/%2f")
}


def main():
    with ClusterRpcProxy(CONFIG) as rpc:
        # Example URLs
        urls = ["https://deno.com/blog/v2.0"]
        # Call the Nameko service's RPC method
        result = rpc.tech_news_service.generate_article(length=3000, references=urls)
        print(result, flush=True)


if __name__ == "__main__":
    main()
