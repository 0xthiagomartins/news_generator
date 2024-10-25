# Technews generator
from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.prompts import BasePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.documents import Document
from langchain_community.document_loaders import BSHTMLLoader
import requests
from bs4 import BeautifulSoup
from .base import BaseConfig


class TechNewsGenerator:
    prompt: BasePromptTemplate = PromptTemplate(
        template=(
            "Você é um redator profissional contratado pela {business_name}. "
            "A empresa é especializada em {scope}. Eles oferecem serviços de {services}. "
            "Os clientes alvo são {target_clients}. "
            "Forneça um artigo bem estruturado e envolvente."
            "{reference_section} "
            "Escreva um artigo noticiário com o título de {article_topic} com o tamanho de {article_length}."
        ),
        input_variables=[
            "business_name",
            "scope",
            "services",
            "target_clients",
            "article_topic",
            "article_length",
            "reference_section",
        ],
    )
    config: BaseConfig = BaseConfig(
        business_name="Nassim Tecnologia",
        scope="Tecnologia, Software, Hardware, Startups",
        services=[
            "Desenvolvimento Web",
            "Search Engine Optimization",
            "Design de Produto",
            "Design de Marca",
            "Automações",
            "Integrações de sistemas",
            "Implementação de Inteligência Artificial",
        ],
        target_clients=[],
    )

    def __init__(self, llm: str = "gemini-1.5-flash"):
        self.chain: Runnable = self.prompt | ChatGoogleGenerativeAI(model=llm)

    def load_references(self, references: list[str]) -> str:
        """Carrega e formata as referências fornecidas, suportando URLs e caminhos de arquivo."""
        references_section = ""
        for reference in references:
            references_section = (
                "Use as seguintes referências para informar sua escrita:\n"
            )
            if reference.startswith("http://") or reference.startswith("https://"):
                # Faz o download do conteúdo HTML da URL
                response = requests.get(reference)
                response.raise_for_status()  # Levanta uma exceção para erros de requisição
                html_content = response.text
                soup = BeautifulSoup(html_content, "html.parser")
                text = soup.get_text()
                references_section += f"{text}\n"
            else:
                # Carrega conteúdo de um arquivo local
                loader = BSHTMLLoader(reference)
                docs: list[Document] = loader.load()
                for doc in docs:
                    references_section += f"{doc.page_content}\n"

        return references_section

    def generate(
        self, topic: str, length: int = 3000, references: list[str] = None
    ) -> str:
        references_section = self.load_references(references) if references else ""

        formatted_prompt = dict(
            business_name=self.config.business_name,
            scope=self.config.scope,
            services=", ".join(self.config.services),
            target_clients=", ".join(self.config.target_clients),
            article_topic=topic,
            article_length=length,
            reference_section=references_section,
        )

        ai_message: AIMessage = self.chain.invoke(formatted_prompt)
        content = ai_message.to_json().get("kwargs", {}).get("content", "")
        markdown_content = f"# {topic}\n\n{content}"
        return markdown_content
