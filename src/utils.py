import requests
from markdownify import markdownify as md


def url_2_md(url: str) -> str:
    """
    It receives a url of a website and returns that website as a markdown.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError(f"Error fetching the URL: {e}")

    html_content = response.text
    markdown = md(html_content)
    return markdown


if __name__ == "__main__":
    from rich import print

    print(url_2_md(input("URL: ")))
