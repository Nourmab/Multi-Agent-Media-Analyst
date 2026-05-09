from agents.text_agent import TextAgent
from agents.image_agent import ImageAgent
from utils.helpers import load_image_as_base64
from concurrent.futures import ThreadPoolExecutor


class Orchestrator:
    """
    Orchestrator — routes tasks to the correct agent,
    runs them in parallel, and merges the results.
    """

    def __init__(self):
        self.text_agent = TextAgent()
        self.image_agent = ImageAgent()

    def _run_text(self, article: dict) -> dict:
        return self.text_agent.analyze(
            title=article["title"],
            content=article["content"],
        )

    def _run_image(self, article: dict) -> dict:
        image_b64 = load_image_as_base64(article["image_url"])
        if not image_b64:
            return {"error": "Could not load image"}
        return self.image_agent.analyze(image_b64)

    def _cross_modal_insight(self, text_result: dict, image_result: dict) -> str:
        """Generate a simple cross-modal insight from both agent results."""
        if "error" in text_result or "error" in image_result:
            return "Could not generate insight due to an agent error."

        sentiment = text_result.get("sentiment", "neutral")
        mood = image_result.get("mood", "neutral")
        caption = image_result.get("caption", "")
        keywords = ", ".join(text_result.get("keywords", []))

        if sentiment == mood or (sentiment == "negative" and mood == "tense"):
            alignment = "The image mood aligns with the article sentiment"
        else:
            alignment = "The image mood contrasts with the article sentiment"

        return (
            f"{alignment} ({sentiment} text / {mood} image). "
            f"Key topics: {keywords}. "
            f"Visual context: {caption}"
        )

    def run(self, article: dict) -> dict:
        """Run both agents in parallel and return the merged report."""
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_text = executor.submit(self._run_text, article)
            future_image = executor.submit(self._run_image, article)
            text_result = future_text.result()
            image_result = future_image.result()

        return {
            "article": {
                "title": article["title"],
                "source": article["source"],
                "url": article["url"],
                "image_url": article["image_url"],
            },
            "text_analysis": text_result,
            "image_analysis": image_result,
            "cross_modal_insight": self._cross_modal_insight(text_result, image_result),
        }