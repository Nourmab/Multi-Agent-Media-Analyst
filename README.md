# 🧠 Multi-Agent Media Analyst

A multi-agent AI system that analyzes news articles using two specialized agents running in parallel — one for text, one for images — orchestrated through LangChain and served via a Streamlit web interface.

---

## 🏗️ Architecture

```
NewsAPI
   │
   ▼
fetch_news()  ──►  article { title, content, image_url }
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
     Text Agent               Image Agent
  (Groq / LLaMA-3)       (Gemini 2.5 Flash)
  summary, sentiment,     caption, objects,
  keywords, category       mood, OCR text
            │                       │
            └───────────┬───────────┘
                        ▼
                  Orchestrator
              cross_modal_insight
                        │
                        ▼
              Streamlit UI → report
```

---

## ✨ Features

- **Text Agent** — powered by Groq / LLaMA-3 via LangChain
  - Article summarization (3 sentences)
  - Sentiment analysis with confidence score
  - Keyword extraction (top 5)
  - Topic category classification

- **Image Agent** — powered by Gemini 2.5 Flash via LangChain
  - Automatic image captioning
  - Object and scene detection
  - Image mood analysis
  - OCR (reads text visible in images)

- **Orchestrator** — runs both agents in parallel via `ThreadPoolExecutor`, then generates a cross-modal insight that neither agent could produce alone

- **Streamlit UI** — clean web interface with article selector, side-by-side results, and raw JSON export

---

## 🗂️ Project Structure

```
media-analyst/
├── agents/
│   ├── __init__.py
│   ├── text_agent.py       # LangChain chain → Groq / LLaMA-3
│   ├── image_agent.py      # LangChain chain → Gemini 2.5 Flash
│   └── orchestrator.py     # Parallel routing + result merging
├── utils/
│   ├── __init__.py
│   └── helpers.py          # NewsAPI fetch + image base64 encoding
├── app.py                  # Streamlit entry point
├── .env                    # API keys (gitignored)
├── .env.example            # Keys template — safe to commit
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Tool | Free tier |
|---|---|---|
| Frontend | Streamlit | ✅ |
| Orchestration | LangChain | ✅ |
| Text Agent LLM | Groq / LLaMA-3.3-70b | ✅ |
| Image Agent LLM | Gemini 2.5 Flash | ✅ |
| News data | NewsAPI | ✅ 100 req/day |
| Language | Python 3.11+ | ✅ |

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/media-analyst.git
cd media-analyst
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up API keys

Copy the example file and fill in your keys:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
NEWS_API_KEY=your_newsapi_key_here
```

Get your free keys here:
- **Groq** → [console.groq.com](https://console.groq.com)
- **Gemini** → [aistudio.google.com](https://aistudio.google.com)
- **NewsAPI** → [newsapi.org/register](https://newsapi.org/register)

### 5. Run the app

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 📊 Output Example

```json
{
  "article": {
    "title": "OpenAI announces new model",
    "source": "TechCrunch",
    "url": "https://..."
  },
  "text_analysis": {
    "summary": "OpenAI unveiled a new model...",
    "sentiment": "positive",
    "sentiment_score": 0.82,
    "keywords": ["OpenAI", "GPT", "AI", "model", "launch"],
    "category": "technology"
  },
  "image_analysis": {
    "caption": "A presenter standing in front of a large screen showing AI graphics",
    "objects": ["person", "screen", "audience", "podium"],
    "scene": "indoor",
    "ocr_text": "OpenAI DevDay 2026",
    "mood": "celebratory"
  },
  "cross_modal_insight": "Image mood aligns with article sentiment (positive text / celebratory image). Key topics: OpenAI, GPT, AI, model, launch. Visual context: A presenter standing in front of a large screen showing AI graphics."
}
```

---

## 🧠 Key Agentic Patterns

**Structured output** — agents are prompted to return strict JSON, making their output reliable and parseable by the orchestrator.

**Agent specialization** — each agent uses the model best suited for its modality (LLaMA-3 for text NLP, Gemini for vision).

**Parallel execution** — both agents run simultaneously via `ThreadPoolExecutor`, cutting response time roughly in half.

**Orchestrator pattern** — a single coordinator owns all agents, routes tasks, and merges results. Agents are fully isolated from each other.

---

## 🗺️ What to Learn Next

- **LangGraph** — add memory, state, and conditional routing between agents
- **CrewAI** — higher-level multi-agent framework with role-based agents
- **Tool use / function calling** — give agents the ability to call APIs autonomously
- **RAG** — add long-term knowledge bases to your agents
- **LangSmith** — trace and debug your LangChain agent chains

---

## 📄 License

MIT — free to use, modify, and distribute.
