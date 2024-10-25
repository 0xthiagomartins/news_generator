# Tech News Generator

## Description

The **Tech News Generator** is a Python-based tool designed to create structured and engaging technology news articles. Leveraging the power of LangChain and Google Generative AI, this tool allows users to generate comprehensive articles based on specific topics and references, which can include both URLs and local documents.

## Features

- **Automated Article Generation:** Create well-structured tech news articles by specifying topics, length, and reference materials.
- **Reference Integration:** Incorporate content from provided URLs or local files to enhance article relevance and accuracy.
- **URL to Markdown Conversion:** Convert web page content into Markdown format for easy integration and editing.
- **Configurable Settings:** Easily adjust configurations like business name, scope, services, and target clients through environment variables.
- **Testing Suite:** Ensure reliability and correctness with pytest-based tests.

## Configuration

Configurations are managed through the `BaseConfig` class located in `src/generators/base.py` and the `.env` file.

### BaseConfig Parameters

- `business_name`: Name of the business (e.g., "Nassim Tecnologia").
- `scope`: Areas of expertise (e.g., "Tecnologia, Software, Hardware, Startups").
- `services`: List of services offered.
- `target_clients`: List of target clients.

These can be adjusted directly in the `BaseConfig` or through environment variables as needed.

## Testing

The project includes a testing suite using `pytest` to ensure the functionality of the `TechNewsGenerator`.

### Running Tests

1. Ensure that you are in the project's root directory and the virtual environment is activated.
2. Execute the following command:

```bash
pytest
```