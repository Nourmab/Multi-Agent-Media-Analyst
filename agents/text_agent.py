from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import os


class TextAgent:
    """
    Text Agent — powered by Groq (LLaMA 3).
    Performs: summarization, sentiment analysis, keyword extraction.
    """

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.2,
        )
        self.parser = StrOutputParser()
        self._build_chain()

    def _build_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a professional news analyst. 
                Given a news article, return ONLY a valid JSON object with no extra text, no markdown, no backticks.
                The JSON must have exactly these fields:
                {{
                  "summary": "3-sentence summary of the article",
                  "sentiment": "positive | negative | neutral",
                  "sentiment_score": 0.0 to 1.0,
                  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
                  "category": "politics | technology | business | sports | health | entertainment | other"
                }}"""
            ),
            (
                "human",
                "Article title: {title}\n\nArticle content:\n{content}"
            ),
        ])
        self.chain = prompt | self.llm | self.parser

    def analyze(self, title: str, content: str) -> dict:
        """Run the text analysis chain and return structured results."""
        try:
            raw = self.chain.invoke({"title": title, "content": content})
            # Clean possible markdown fences just in case
            clean = raw.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {e}", "raw": raw}
        except Exception as e:
            return {"error": str(e)}