import streamlit as st
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dani — Humanized Summarizer",
    page_icon="✦",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@300;400&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">

<style>
/* ── Global reset & theme ── */
html, body, [class*="css"] {
    background-color: #0e0e0e !important;
    color: #e8e3db !important;
}

.stApp {
    background-color: #0e0e0e;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2rem; padding-bottom: 4rem; max-width: 820px; }

/* ── Header ── */
.distill-header {
    text-align: center;
    margin-bottom: 48px;
    padding-top: 24px;
}
.logo-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 16px;
}
.diamond {
    width: 9px; height: 9px;
    background: #d4a853;
    transform: rotate(45deg);
    display: inline-block;
    animation: pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%,100%{opacity:1;transform:rotate(45deg) scale(1)}
    50%{opacity:.55;transform:rotate(45deg) scale(.82)}
}
.logo-wordmark {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: .3em;
    color: #d4a853;
    text-transform: uppercase;
    font-weight: 300;
}
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(32px, 5vw, 52px);
    font-weight: 400;
    line-height: 1.1;
    color: #e8e3db;
    margin-bottom: 12px;
}
.main-title em { font-style: italic; color: #d4a853; }
.subtitle {
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    color: #7a7570;
    letter-spacing: .02em;
    line-height: 1.6;
    font-weight: 300;
}

/* ── Section labels ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: #4a4540;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
    margin-top: 20px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #2a2a2a;
}

/* ── Textarea ── */
.stTextArea textarea {
    background: #161616 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 4px !important;
    color: #e8e3db !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    font-weight: 300 !important;
    line-height: 1.75 !important;
    resize: vertical !important;
}
.stTextArea textarea:focus {
    border-color: #b5895c !important;
    box-shadow: 0 0 0 3px rgba(212,168,83,.07) !important;
}
.stTextArea textarea::placeholder { color: #4a4540 !important; }

/* ── Radio buttons → pill toggle ── */
.stRadio > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 8px !important;
    flex-wrap: wrap !important;
}
.stRadio label {
    background: transparent !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 2px !important;
    padding: 7px 16px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: .1em !important;
    color: #7a7570 !important;
    cursor: pointer !important;
    transition: all .2s !important;
}
.stRadio label:hover { border-color: #b5895c !important; color: #e8e3db !important; }
.stRadio [data-checked="true"] label,
.stRadio input:checked + div {
    background: #d4a853 !important;
    border-color: #d4a853 !important;
    color: #0e0e0e !important;
}
/* hide the actual radio dot */
.stRadio input[type="radio"] { display: none !important; }

/* ── Button ── */
.stButton button {
    width: 100% !important;
    padding: 18px !important;
    background: #d4a853 !important;
    border: none !important;
    border-radius: 4px !important;
    color: #0e0e0e !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    letter-spacing: .08em !important;
    transition: all .25s !important;
    margin-top: 12px !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(212,168,83,.25) !important;
    background: #dbb85f !important;
}

/* ── Output card ── */
.output-card {
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 4px;
    overflow: hidden;
    margin-top: 8px;
    animation: fadeUp .5s ease both;
}
@keyframes fadeUp {
    from{opacity:0;transform:translateY(14px)}
    to{opacity:1;transform:translateY(0)}
}
.output-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 20px;
    border-bottom: 1px solid #2a2a2a;
    background: #1f1f1f;
}
.output-tag {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: .2em;
    color: #d4a853;
    text-transform: uppercase;
}
.output-body {
    padding: 26px 24px;
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    line-height: 1.85;
    color: #e8e3db;
}
.stats-row {
    display: flex;
    gap: 28px;
    padding: 14px 20px;
    border-top: 1px solid #2a2a2a;
    background: #1f1f1f;
}
.stat { display: flex; flex-direction: column; gap: 3px; }
.stat-val {
    font-family: 'DM Mono', monospace;
    font-size: 16px;
    color: #d4a853;
}
.stat-label {
    font-size: 10px;
    letter-spacing: .1em;
    color: #4a4540;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
}

/* ── Error ── */
.stAlert {
    background: rgba(180,60,60,.1) !important;
    border: 1px solid rgba(180,60,60,.3) !important;
    border-radius: 4px !important;
    color: #e07070 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 13px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #d4a853 !important; }

/* ── Footer ── */
.distill-footer {
    text-align: center;
    margin-top: 60px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: .2em;
    color: #4a4540;
}

/* ── Columns gap fix ── */
[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="distill-header">
  <div class="logo-row">
    <div class="diamond"></div>
    <span class="logo-wordmark">Dani_Tech</span>
    <div class="diamond"></div>
  </div>
  <div class="main-title">Text made <em>human.</em></div>
  <div class="subtitle">Paste any text. Get a clear, warm, humanized summary — not robotic output.</div>
</div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your text</div>', unsafe_allow_html=True)
input_text = st.text_area(
    label="",
    height=220,
    placeholder="Paste an article, report, email thread, research paper, or any block of text you'd like summarized...",
    label_visibility="collapsed",
)

if input_text.strip():
    wc = len(input_text.strip().split())
    st.caption(f"✦ {wc:,} words")

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

# ── Summarize button ──────────────────────────────────────────────────────────
st.markdown("")
clicked = st.button("✦ Distill this text →", use_container_width=True)

# ── Logic ─────────────────────────────────────────────────────────────────────
if clicked:
    if not input_text.strip():
        st.error("Please paste some text to summarize.")
    elif len(input_text.strip().split()) < 20:
        st.error("Text is too short — please provide at least 20 words.")
    else:
        length_guide = {
            "Concise": "in 2–4 sentences",
            "Balanced": "in 1–2 short paragraphs",
            "Detailed": "in 2–3 paragraphs with key details preserved",
        }[length]

        tone_guide = {
            "Conversational": "warm, clear, and conversational — like explaining to a smart friend",
            "Professional": "polished and professional, suitable for a business context",
            "Casual": "casual and relaxed, like a quick chat message",
            "Empathetic": "warm, empathetic, and human-centered — acknowledging the human side of the content",
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
            # API key from Streamlit secrets (st.secrets) or fallback to env
            api_key = st.secrets.get("ANTHROPIC_API_KEY", None)
            client = anthropic.Anthropic(api_key=api_key) if api_key else anthropic.Anthropic()

            with st.spinner("Distilling your text..."):
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )

            summary = response.content[0].text

            # Stats
            orig_words = len(input_text.strip().split())
            summ_words = len(summary.strip().split())
            reduction = round((1 - summ_words / orig_words) * 100)

            # Output card
            st.markdown('<div class="section-label">Summary</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="output-card">
              <div class="output-header">
                <span class="output-tag">✦ {tone} Summary</span>
              </div>
              <div class="output-body">{summary}</div>
              <div class="stats-row">
                <div class="stat">
                  <span class="stat-val">{orig_words:,}</span>
                  <span class="stat-label">Original words</span>
                </div>
                <div class="stat">
                  <span class="stat-val">{summ_words:,}</span>
                  <span class="stat-label">Summary words</span>
                </div>
                <div class="stat">
                  <span class="stat-val">{reduction}%</span>
                  <span class="stat-label">Reduction</span>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Copy-friendly text area below card
            st.text_area("Copy summary:", value=summary, height=120, key="copy_area")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="distill-footer">
  Powered by Agentic AI · Built with Streamlit · No data stored
</div>
""", unsafe_allow_html=True)
