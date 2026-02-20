# ✦ Distill — Humanized Text Summarizer

A beautiful, dark-themed text summarizer powered by Claude AI. Paste any text and get a warm, natural, human-sounding summary — not robotic output.

## Features

- 🎨 **4 tone options** — Conversational, Professional, Casual, Empathetic  
- 📏 **3 length options** — Concise, Balanced, Detailed  
- 📊 **Word reduction stats** — see how much was compressed  
- ✦ Powered by Claude (Anthropic)

## Deploy on Streamlit Cloud

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your GitHub
3. Select this repo, set `app.py` as the entry point
4. Under **Settings → Secrets**, add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Click **Deploy** 🚀

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml` with your API key (see above).

## Stack

- [Streamlit](https://streamlit.io) — UI framework  
- [Anthropic Python SDK](https://github.com/anthropic-ai/anthropic-python) — Claude API  
