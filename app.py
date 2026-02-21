import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LUMINA",
    page_icon="✿",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@300;400;500&family=Courier+Prime:ital,wght@0,400;1,400&display=swap" rel="stylesheet">

<style>

/* ── Base ── */
html, body, [class*="css"] {
    background-color: #f7f2eb !important;
    color: #2c2118 !important;
    font-family: 'Jost', sans-serif !important;
}

.stApp {
    background: #f7f2eb;
    background-image:
        radial-gradient(ellipse at 10% 0%, rgba(196,140,100,0.12) 0%, transparent 55%),
        radial-gradient(ellipse at 90% 100%, rgba(180,120,80,0.10) 0%, transparent 55%);
    min-height: 100vh;
}

/* hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 5rem;
    max-width: 800px;
}

/* ── Decorative top border ── */
.stApp::before {
    content: '';
    display: block;
    height: 4px;
    background: linear-gradient(90deg, #c48c64, #e8b48a, #c48c64);
    position: fixed;
    top: 0; left: 0; right: 0;
    z-index: 999;
}

/* ── Header ── */
.dani-header {
    text-align: center;
    margin-bottom: 52px;
    padding-top: 20px;
    position: relative;
}

.header-ornament {
    font-family: 'Courier Prime', monospace;
    font-size: 13px;
    color: #c48c64;
    letter-spacing: 0.4em;
    margin-bottom: 18px;
    display: block;
}

.main-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(42px, 7vw, 72px);
    font-weight: 300;
    line-height: 1.0;
    color: #2c2118;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
}

.main-title span {
    font-style: italic;
    color: #c48c64;
}

.tagline {
    font-family: 'Jost', sans-serif;
    font-size: 13px;
    font-weight: 300;
    color: #8a7060;
    letter-spacing: 0.06em;
    margin-top: 14px;
    line-height: 1.7;
}

.header-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin: 20px auto 0;
    color: #c48c64;
    font-size: 12px;
    letter-spacing: 0.3em;
}

.header-divider::before,
.header-divider::after {
    content: '';
    width: 60px;
    height: 1px;
    background: linear-gradient(90deg, transparent, #c48c64);
}

.header-divider::after {
    background: linear-gradient(90deg, #c48c64, transparent);
}

/* ── Section labels ── */
.section-label {
    font-family: 'Courier Prime', monospace;
    font-size: 10px;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #b09080;
    margin-bottom: 8px;
    margin-top: 22px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #e0d4c4, transparent);
}

/* ── Textarea ── */
.stTextArea textarea {
    background: #fdf9f4 !important;
    border: 1.5px solid #e0d0bc !important;
    border-radius: 6px !important;
    color: #2c2118 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 15px !important;
    font-weight: 300 !important;
    line-height: 1.8 !important;
    padding: 18px 20px !important;
    box-shadow: inset 0 2px 8px rgba(180,140,100,0.05), 0 2px 12px rgba(180,140,100,0.08) !important;
    transition: all 0.25s !important;
}
.stTextArea textarea:focus {
    border-color: #c48c64 !important;
    box-shadow: inset 0 2px 8px rgba(180,140,100,0.05), 0 0 0 3px rgba(196,140,100,0.12) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #c8b8a4 !important; }

/* ── Radio (pill toggles) ── */
.stRadio > label { display: none !important; }
.stRadio > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
}
.stRadio label {
    background: #fdf9f4 !important;
    border: 1.5px solid #e0d0bc !important;
    border-radius: 30px !important;
    padding: 7px 18px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 12px !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    color: #8a7060 !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    box-shadow: 0 1px 4px rgba(180,140,100,0.08) !important;
}
.stRadio label:hover {
    border-color: #c48c64 !important;
    color: #c48c64 !important;
    background: #fef7f0 !important;
}
.stRadio [data-checked="true"] > label,
.stRadio input:checked ~ div > label {
    background: #c48c64 !important;
    border-color: #c48c64 !important;
    color: #fff8f2 !important;
    box-shadow: 0 3px 10px rgba(196,140,100,0.3) !important;
}
.stRadio input[type="radio"] { display: none !important; }

/* ── Caption / word count ── */
.stCaption {
    font-family: 'Courier Prime', monospace !important;
    font-size: 11px !important;
    color: #b09080 !important;
    text-align: right !important;
    letter-spacing: 0.05em !important;
}

/* ── Button ── */
.stButton button {
    width: 100% !important;
    padding: 17px 24px !important;
    background: linear-gradient(135deg, #c48c64 0%, #b87a52 100%) !important;
    border: none !important;
    border-radius: 6px !important;
    color: #fff8f2 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 16px rgba(180,120,80,0.25) !important;
    margin-top: 14px !important;
}
.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(180,120,80,0.35) !important;
    background: linear-gradient(135deg, #cf9870 0%, #c48c64 100%) !important;
}
.stButton button:active {
    transform: translateY(0) !important;
}

/* ── Output card ── */
.output-wrap {
    margin-top: 10px;
    animation: riseUp 0.5s cubic-bezier(0.22, 1, 0.36, 1) both;
}
@keyframes riseUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}

.output-card {
    background: #fdf9f4;
    border: 1.5px solid #e0d0bc;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(180,140,100,0.12), 0 2px 8px rgba(180,140,100,0.08);
}

.output-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 22px;
    background: linear-gradient(135deg, #f5ede0 0%, #f0e6d4 100%);
    border-bottom: 1px solid #e8d8c4;
}

.output-badge {
    font-family: 'Courier Prime', monospace;
    font-size: 10px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c48c64;
    display: flex;
    align-items: center;
    gap: 7px;
}

.output-badge::before {
    content: '✿';
    font-size: 12px;
}

.output-body {
    padding: 28px 26px 22px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 18px;
    line-height: 1.9;
    color: #2c2118;
    font-weight: 300;
    letter-spacing: 0.01em;
}

.stats-row {
    display: flex;
    gap: 0;
    border-top: 1px solid #e8d8c4;
    background: linear-gradient(135deg, #f5ede0, #f0e6d4);
}

.stat {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 14px 0;
    gap: 4px;
    border-right: 1px solid #e8d8c4;
}
.stat:last-child { border-right: none; }

.stat-val {
    font-family: 'Cormorant Garamond', serif;
    font-size: 22px;
    font-weight: 600;
    color: #c48c64;
    line-height: 1;
}

.stat-label {
    font-family: 'Courier Prime', monospace;
    font-size: 9px;
    letter-spacing: 0.18em;
    color: #b09080;
    text-transform: uppercase;
}

/* ── Copy textarea ── */
.stTextArea [data-baseweb="textarea"] textarea {
    font-size: 13px !important;
    background: #fdf9f4 !important;
    color: #6a5a4a !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #c48c64 !important;
}

/* ── Alerts ── */
.stAlert {
    background: rgba(196,100,80,0.08) !important;
    border: 1.5px solid rgba(196,100,80,0.25) !important;
    border-radius: 6px !important;
    color: #a04030 !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 13px !important;
}

/* ── Footer ── */
.dani-footer {
    text-align: center;
    margin-top: 64px;
    padding-top: 24px;
    border-top: 1px solid #e0d0bc;
}

.footer-ornament {
    font-family: 'Courier Prime', monospace;
    font-size: 10px;
    letter-spacing: 0.3em;
    color: #c8b4a0;
    text-transform: uppercase;
}

/* ── Columns ── */
[data-testid="column"] { padding: 0 8px !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dani-header">
  <span class="header-ornament">✦ &nbsp; Told by Dani &nbsp; ✦</span>
  <div class="main-title">LUMINA</div>
  <div class="tagline">
    Paste any text. Receive a clear, warm, humanized summary<br>that actually sounds like a person wrote it.
  </div>
  <div class="header-divider">✿</div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your text</div>', unsafe_allow_html=True)
input_text = st.text_area(
    label="input",
    height=230,
    placeholder="Paste an article, report, email, research paper, or any block of text you'd like to distill into something readable...",
    label_visibility="collapsed",
)

if input_text.strip():
    wc = len(input_text.strip().split())
    st.caption(f"✦  {wc:,} words")

# ── Controls ──────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">Tone</div>', unsafe_allow_html=True)
    tone = st.radio(
        "Tone",
        ["Conversational", "Professional", "Casual", "Empathetic"],
        horizontal=True,
        label_visibility="collapsed",
    )

with col2:
    st.markdown('<div class="section-label">Length</div>', unsafe_allow_html=True)
    length = st.radio(
        "Length",
        ["Concise", "Balanced", "Detailed"],
        horizontal=True,
        label_visibility="collapsed",
    )

# ── Button ────────────────────────────────────────────────────────────────────
st.markdown("")
clicked = st.button("✦  Summarize this text", use_container_width=True)

# ── Logic ─────────────────────────────────────────────────────────────────────
if clicked:
    if not input_text.strip():
        st.error("Please paste some text to summarize.")
    elif len(input_text.strip().split()) < 20:
        st.error("Text is too short — please provide at least 20 words.")
    else:
        length_guide = {
            "Concise":  "in 2–4 sentences",
            "Balanced": "in 1–2 short paragraphs",
            "Detailed": "in 2–3 paragraphs with key details preserved",
        }[length]

        tone_guide = {
            "Conversational": "warm, clear, and conversational — like explaining to a smart friend",
            "Professional":   "polished and professional, suitable for a business context",
            "Casual":         "casual and relaxed, like a quick chat message",
            "Empathetic":     "warm, empathetic, and human-centered — acknowledging the human side of the content",
        }[tone]

        system_prompt = (
            "You are an expert at creating humanized, natural-sounding summaries. "
            "Your summaries never sound robotic or AI-generated. They read like something "
            "a thoughtful person would write. You capture the essence and spirit of text, "
            "not just the facts. Avoid bullet points, jargon, or sterile language."
        )

        user_prompt = (
            f"Please summarize the following text {length_guide}. "
            f"Write in a {tone_guide} tone. Make it feel natural and human — "
            "no robotic phrasing, no 'The text discusses...' openers. "
            "Just get right into the summary as if you're telling someone about it.\n\n"
            f"Text:\n{input_text}"
        )

        try:
            try:
                api_key = st.secrets["GROQ_API_KEY"]
            except (KeyError, FileNotFoundError):
                st.error("⚠️ API key not found. Please add GROQ_API_KEY to your Streamlit secrets.")
                st.stop()

            with st.spinner("Crafting your summary..."):
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt},
                        ],
                        "max_tokens": 1000,
                    },
                    timeout=30,
                )
                response.raise_for_status()

            summary = response.json()["choices"][0]["message"]["content"]

            orig_words = len(input_text.strip().split())
            summ_words = len(summary.strip().split())
            reduction  = round((1 - summ_words / orig_words) * 100)

            # Output card
            st.markdown('<div class="section-label">Your summary</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="output-wrap">
              <div class="output-card">
                <div class="output-top">
                  <span class="output-badge">{tone} · {length}</span>
                </div>
                <div class="output-body">{summary}</div>
                <div class="stats-row">
                  <div class="stat">
                    <span class="stat-val">{orig_words:,}</span>
                    <span class="stat-label">Original</span>
                  </div>
                  <div class="stat">
                    <span class="stat-val">{summ_words:,}</span>
                    <span class="stat-label">Summary</span>
                  </div>
                  <div class="stat">
                    <span class="stat-val">{reduction}%</span>
                    <span class="stat-label">Shorter</span>
                  </div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-label">Copy text</div>', unsafe_allow_html=True)
            st.text_area("copy", value=summary, height=110, label_visibility="collapsed", key="copy_out")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="dani-footer">
  <div class="footer-ornament">✿ &nbsp; LUMINA &nbsp; · &nbsp; Powered by Groq · Llama 3.3 &nbsp; · &nbsp; No data stored &nbsp; ✿</div>
</div>
""", unsafe_allow_html=True)
