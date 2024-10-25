import pytest
from src.generators.tech_news import TechNewsGenerator
from rich import print


def test_generate():
    generator = TechNewsGenerator(llm="gemini-1.5-pro")
    # Act
    result = generator.generate(
        topic="Backend",
        length=3000,
        references=["https://www.nassim.com.br/blog/pt-ms"],
    )
    print(result, flush=True)
    assert isinstance(result, str)
