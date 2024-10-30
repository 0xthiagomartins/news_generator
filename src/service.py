from nameko.rpc import rpc
from src.generators.tech_news import TechNewsGenerator
from dotenv import load_dotenv

load_dotenv(dotenv_path="./resources/.env")


class NewsGenerator:
    name = "news_generator"

    @rpc
    def generate(
        self,
        urls: list = [],
        llm: str = "gemini-1.5-pro",
        length: int = 3000,
        custom_prompt: str = "",
        temperature: float = 0.7,
    ):
        generator = TechNewsGenerator(
            llm=llm if llm else "gemini-1.5-pro", 
            custom_prompt=custom_prompt,
            temperature=temperature
        )
        result = generator.generate(
            length=length,
            references=urls,
        )
        return result
