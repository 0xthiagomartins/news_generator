from nameko.rpc import rpc
from src.generators.tech_news import TechNewsGenerator
from dotenv import load_dotenv

load_dotenv(dotenv_path="./resources/.env")


class NewsGenerator:
    name = "news_generator"

    @rpc
    def generate(self, urls: list = [], length: int = 3000):
        generator = TechNewsGenerator(llm="gemini-1.5-pro")
        result = generator.generate(
            length=length,
            references=urls,
        )
        return result
