import streamlit as st
from dotenv import load_dotenv
from agents.orchestrator import Orchestrator
from utils.helpers import fetch_news
import os
import json
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


load_dotenv()

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Media Analyst",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Multi-Agent Media Analyst")
st.caption("Text Agent (Groq/LLaMA 3) + Image Agent (Gemini 1.5 Flash) — powered by LangChain")

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    query = st.text_input("Search topic", value="artificial intelligence")
    language = st.selectbox("Language", ["en", "fr", "ar"], index=0)
    if st.button("🔍 Fetch Articles", use_container_width=True):
        with st.spinner("Fetching news..."):
            articles = fetch_news(
                api_key=os.getenv("NEWS_API_KEY"),
                query=query,
                language=language,
            )
            st.session_state["articles"] = articles
            st.session_state["report"] = None
        if articles:
            st.success(f"Found {len(articles)} articles")
        else:
            st.warning("No articles found. Try a different query.")

# ── Article selector ──────────────────────────────────────────
if "articles" in st.session_state and st.session_state["articles"]:
    articles = st.session_state["articles"]
    titles = [a["title"] for a in articles]
    selected_title = st.selectbox("Select an article to analyze", titles)
    selected = next(a for a in articles if a["title"] == selected_title)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📰 Article")
        st.markdown(f"**Source:** {selected['source']} | [Read full article]({selected['url']})")
        st.write(selected["content"][:800] + "...")
    with col2:
        st.subheader("🖼️ Image")
        st.image(selected["image_url"], use_column_width=True)

    if st.button("🚀 Run Multi-Agent Analysis", use_container_width=True, type="primary"):
        orchestrator = Orchestrator()
        with st.spinner("Running agents in parallel..."):
            report = orchestrator.run(selected)
            st.session_state["report"] = report

# ── Report display ─────────────────────────────────────────────
if "report" in st.session_state and st.session_state.get("report"):
    report = st.session_state["report"]
    st.divider()
    st.subheader("📊 Analysis Report")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📝 Text Agent")
        ta = report.get("text_analysis", {})
        if "error" not in ta:
            sentiment_color = {"positive": "🟢", "negative": "🔴", "neutral": "🟡"}
            emoji = sentiment_color.get(ta.get("sentiment", "neutral"), "🟡")
            st.metric("Sentiment", f"{emoji} {ta.get('sentiment', 'N/A').capitalize()}", f"Score: {ta.get('sentiment_score', 0):.2f}")
            st.metric("Category", ta.get("category", "N/A").capitalize())
            st.markdown("**Summary:**")
            st.info(ta.get("summary", "N/A"))
            st.markdown("**Keywords:**")
            st.write(" · ".join([f"`{k}`" for k in ta.get("keywords", [])]))
        else:
            st.error(f"Text Agent error: {ta['error']}")

    with col2:
        st.markdown("### 🖼️ Image Agent")
        ia = report.get("image_analysis", {})
        if "error" not in ia:
            st.metric("Scene", ia.get("scene", "N/A").capitalize())
            st.metric("Mood", ia.get("mood", "N/A").capitalize())
            st.markdown("**Caption:**")
            st.info(ia.get("caption", "N/A"))
            st.markdown("**Detected objects:**")
            st.write(" · ".join([f"`{o}`" for o in ia.get("objects", [])]))
            if ia.get("ocr_text"):
                st.markdown("**Text in image (OCR):**")
                st.code(ia.get("ocr_text"))
        else:
            st.error(f"Image Agent error: {ia['error']}")

    st.divider()
    st.markdown("### Cross-Modal Insight")
    st.success(report.get("cross_modal_insight", "N/A"))

    with st.expander("🧾 Raw JSON report"):
        st.json(report)