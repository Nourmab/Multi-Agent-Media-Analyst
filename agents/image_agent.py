from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
import json
import os


class ImageAgent:
    """
    Image Agent — powered by Gemini 1.5 Flash.
    Performs: captioning, object detection, OCR, scene classification.
    """

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.2,
        )
        self.parser = StrOutputParser()

    def analyze(self, image_base64: str) -> dict:
        """Run the image analysis chain and return structured results."""
        try:
            message = HumanMessage(
                content=[
                    {
                        "type": "text",
                        "text": """You are a professional image analyst.
                        Analyze this news image and return ONLY a valid JSON object with no extra text, no markdown, no backticks.
                        The JSON must have exactly these fields:
                        {
                          "caption": "one clear sentence describing the image",
                          "objects": ["list", "of", "detected", "objects", "or", "people"],
                          "scene": "indoor | outdoor | studio | other",
                          "ocr_text": "any visible text in the image, or null if none",
                          "mood": "tense | calm | celebratory | sad | neutral | other"
                        }"""
                    },
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_base64}",
                    },
                ]
            )
            raw = self.llm.invoke([message])
            clean = raw.content.strip().removeprefix("```json").removesuffix("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError as e:
            return {"error": f"JSON parse error: {e}"}
        except Exception as e:
            return {"error": str(e)}