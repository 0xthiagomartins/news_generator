# Technews generator
from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.prompts import BasePromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.documents import Document
import requests
from bs4 import BeautifulSoup
from .base import BaseConfig


class TechNewsGenerator:
    prompt: BasePromptTemplate = PromptTemplate(
        template=(
            "Você é um redator profissional contratado pela {business_name}. "
            "A empresa é especializada em {scope}. Eles oferecem serviços de {services}. "
            "Os clientes alvo são {target_clients}. "
            "Use as seguintes referências para informar sua escrita:\n{reference_section}\n\n"
            "Escreva um artigo noticioso bem-estruturado e envolvente com o seguinte tamanho: {article_length} palavras. "
            "O artigo deve incluir os seguintes elementos:\n"
            "1. Título chamativo\n"
            "2. Introdução que captura a atenção do leitor\n"
            "3. Corpo principal dividido em seções com subtítulos\n"
            "4. Conclusão que resume os pontos principais e incentiva a ação\n\n"
            "Considere as melhores práticas de SEO, inserindo palavras-chave relevantes naturalmente ao longo do texto. "
            "Mantenha um tom profissional e informativo, adequado para o público-alvo."
        ),
        input_variables=[
            "business_name",
            "scope",
            "services",
            "target_clients",
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
        references_section = ""
        for reference in references:
            references_section = (
                "Use as seguintes referências para informar sua escrita:\n"
            )
            response = requests.get(reference)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            text = soup.get_text()
            references_section += f"{text}\n"

        return references_section

    def generate(self, length: int = 3000, references: list[str] = None) -> str:
        references_section = self.load_references(references) if references else ""
        formatted_prompt = dict(
            business_name=self.config.business_name,
            scope=self.config.scope,
            services=", ".join(self.config.services),
            target_clients=", ".join(self.config.target_clients),
            article_length=length,
            reference_section=references_section,
        )
        ai_message: AIMessage = self.chain.invoke(formatted_prompt)
        response_data = ai_message.to_json().get("kwargs", {}).get("content", "")

        metadata = {
            "title": "",  # Placeholder para título
            "description": "",  # Placeholder para descrição
            "image": "",  # Placeholder para URL da imagem
            "categories": self.config.categories,  # Utiliza categorias da configuração
        }
        content = response_data

        if response_data.startswith("---"):
            end = response_data.find("---", 3)
            if end != -1:
                front_matter = response_data[3:end].strip()
                for line in front_matter.split("\n"):
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip().strip('"').strip("'")
                    if key in metadata and key != "categories":
                        metadata[key] = value
                content = response_data[end + 3 :].strip()

        markdown_content = (
            f"---\n"
            f"title: \"{metadata['title'][:75]}\"\n"
            f"description: \"{metadata['description'][:255]}\"\n"
            f"image: \"{metadata['image']}\"\n"
            f"categories: {metadata['categories']}\n"
            f"---\n\n"
            f"{content}"
        )
        return markdown_content
