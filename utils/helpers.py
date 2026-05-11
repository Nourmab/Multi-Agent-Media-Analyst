import base64
import requests
from PIL import Image
from io import BytesIO


def load_image_as_base64(image_url: str) -> str | None:
    
    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return encoded
    except Exception as e:
        print(f"[helpers] Failed to load image: {e}")
        return None


def fetch_news(api_key: str, query: str, language: str = "en") -> list[dict]:
    
    from newsapi import NewsApiClient
    client = NewsApiClient(api_key=api_key)
    response = client.get_everything(
        q=query,
        language=language,
        sort_by="publishedAt",
        page_size=5,
    )
    articles = []
    for article in response.get("articles", []):
        if article.get("content") and article.get("urlToImage"):
            articles.append({
                "title": article.get("title", "No title"),
                "content": article.get("content", ""),
                "image_url": article.get("urlToImage", ""),
                "source": article.get("source", {}).get("name", "Unknown"),
                "url": article.get("url", ""),
            })
    return articles