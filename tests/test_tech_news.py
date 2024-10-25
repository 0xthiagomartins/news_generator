import pytest
from src.generators.tech_news import TechNewsGenerator
from rich import print


def test_generate():
    generator = TechNewsGenerator(llm="gemini-1.5-pro")
    # Act
    result = generator.generate(
        length=3000,
        references=["https://deno.com/blog/v2.0"],
    )
    print(result, flush=True)
    assert isinstance(result, str)
