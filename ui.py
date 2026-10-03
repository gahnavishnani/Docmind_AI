# ui.py

import html
import streamlit as st


# =========================================================
# HTML HELPER  (fixes the "code block" rendering bug)
# =========================================================

def flatten(markup: str) -> str:
    """Remove indentation and blank lines so Markdown never
    treats the HTML as a code block."""
    lines = [line.strip() for line in str(markup).splitlines()]
    return "\n".join(line for line in lines if line)


def render_html(markup: str):
    st.markdown(flatten(markup), unsafe_allow_html=True)


def safe_text(value) -> str:
    """Escape text and keep line breaks without blank lines."""
    return html.escape(str(value)).replace("\r", "").replace("\n", "<br>")


# =========================================================
# CSS
# =========================================================

CSS = """
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(124,92,255,0.16), transparent 28%),
        radial-gradient(circle at 90% 90%, rgba(67,220,151,0.05), transparent 25%),
        #07080d;
    color: #f5f5f7;
}
.block-container { max-width: 1250px; padding-top: 2rem; padding-bottom: 5rem; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* NAV */
.dm-nav { display: flex; align-items: center; justify-content: space-between; padding: 10px 0 20px; border-bottom: 1px solid rgba(255,255,255,0.07); margin-bottom: 35px; }
.dm-brand { display: flex; align-items: center; gap: 12px; }
.dm-logo { width: 42px; height: 42px; border-radius: 13px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #a998ff, #7658ff); color: white; font-size: 20px; font-weight: 700; box-shadow: 0 0 35px rgba(118,88,255,0.35); }
.dm-brand-name { color: #f4f4f6; font-size: 17px; font-weight: 700; letter-spacing: -0.5px; }
.dm-brand-subtitle { color: #696d78; font-size: 8px; font-weight: 700; letter-spacing: 1.7px; margin-top: 2px; }
.dm-online { display: flex; align-items: center; gap: 8px; padding: 7px 12px; border-radius: 999px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); color: #858995; font-size: 10px; }
.dm-online-dot { width: 7px; height: 7px; border-radius: 50%; background: #63e6a7; box-shadow: 0 0 12px rgba(99,230,167,0.8); }

/* WELCOME */
.welcome-wrapper { min-height: 72vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; position: relative; }
.welcome-glow { position: absolute; width: 600px; height: 600px; border-radius: 50%; background: radial-gradient(circle, rgba(124,92,255,0.18), transparent 68%); pointer-events: none; filter: blur(8px); }
.welcome-symbol { position: relative; width: 78px; height: 78px; display: flex; align-items: center; justify-content: center; border-radius: 24px; background: linear-gradient(145deg, rgba(132,105,255,0.2), rgba(132,105,255,0.05)); border: 1px solid rgba(132,105,255,0.3); color: #aa9eff; font-size: 28px; box-shadow: 0 0 60px rgba(132,105,255,0.18); margin-bottom: 28px; }
.welcome-brand { position: relative; font-size: clamp(60px, 10vw, 125px); line-height: 0.9; font-weight: 800; letter-spacing: -7px; background: linear-gradient(120deg, #ffffff 5%, #ddd8ff 52%, #8d78ff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.welcome-tagline { position: relative; margin-top: 32px; color: #e8e8ec; font-size: clamp(26px, 4vw, 44px); font-weight: 500; letter-spacing: -1.5px; }
.welcome-description { position: relative; max-width: 540px; margin-top: 17px; color: #858995; font-size: 14px; line-height: 1.8; }
.welcome-flow { position: relative; margin-top: 38px; color: #686c77; font-size: 10px; font-weight: 700; letter-spacing: 2px; }
.welcome-flow span { color: #8c79ff; margin: 0 10px; }

/* HERO */
.hero { text-align: center; padding: 65px 20px 35px; }
.eyebrow { color: #9a89ff; font-size: 9px; font-weight: 700; letter-spacing: 2.5px; }
.hero-title { margin-top: 18px; font-size: clamp(43px, 6vw, 75px); line-height: 1; font-weight: 800; letter-spacing: -4px; background: linear-gradient(120deg, #ffffff, #ddd8ff 55%, #8d78ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-description { max-width: 620px; margin: 22px auto 0; color: #7d818c; font-size: 14px; line-height: 1.8; }

/* UPLOAD */
.upload-card { max-width: 850px; margin: 30px auto; padding: 42px 30px; text-align: center; border-radius: 24px; background: linear-gradient(145deg, rgba(255,255,255,0.055), rgba(255,255,255,0.018)); border: 1px solid rgba(255,255,255,0.09); box-shadow: 0 30px 90px rgba(0,0,0,0.3); }
.upload-icon { width: 65px; height: 65px; display: flex; align-items: center; justify-content: center; margin: 0 auto 18px; border-radius: 20px; background: rgba(124,92,255,0.12); border: 1px solid rgba(124,92,255,0.22); color: #a193ff; font-size: 26px; }
.upload-title { color: #eeeef1; font-size: 23px; font-weight: 600; }
.upload-subtitle { margin-top: 8px; color: #747883; font-size: 12px; }

/* SECTION */
.section-label { margin-top: 35px; margin-bottom: 13px; color: #696d78; font-size: 9px; font-weight: 700; letter-spacing: 1.8px; text-transform: uppercase; }

/* DOCUMENT ROW */
.document-row { display: flex; align-items: center; gap: 14px; padding: 14px 16px; margin-top: 9px; border-radius: 15px; background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07); }
.pdf-icon { width: 42px; height: 42px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; border-radius: 12px; background: rgba(124,92,255,0.12); color: #a193ff; font-size: 9px; font-weight: 800; }
.document-info { flex: 1; min-width: 0; }
.document-name { color: #dadbe0; font-size: 12px; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.document-meta { color: #676b76; font-size: 10px; margin-top: 4px; }
.document-check { color: #63e6a7; font-size: 15px; }

/* PROCESSING */
.processing { max-width: 700px; margin: 100px auto; padding: 65px 30px; text-align: center; border-radius: 24px; background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08); }
.processing-orb { width: 88px; height: 88px; margin: 0 auto 28px; border-radius: 50%; background: radial-gradient(circle at 35% 25%, #d9d3ff, #917cff 35%, #5940d3 65%, #211348); box-shadow: 0 0 65px rgba(124,92,255,0.4); animation: pulse 1.6s ease-in-out infinite; }
@keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.08); } }
.processing-title { color: #eeeef1; font-size: 27px; font-weight: 600; }
.processing-subtitle { margin-top: 9px; color: #727681; font-size: 13px; }

/* SUCCESS */
.success { text-align: center; padding: 35px 10px 25px; }
.success-icon { width: 48px; height: 48px; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: #63e6a7; background: rgba(99,230,167,0.08); border: 1px solid rgba(99,230,167,0.2); }
.success-title { color: #eeeef1; font-size: 30px; font-weight: 600; letter-spacing: -1px; }
.success-description { margin-top: 7px; color: #737782; font-size: 12px; }

/* STATS */
.stat { padding: 20px 12px; text-align: center; border-radius: 17px; background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.07); }
.stat-value { color: #eeeef1; font-size: 23px; font-weight: 700; }
.stat-label { margin-top: 4px; color: #686c77; font-size: 9px; font-weight: 700; letter-spacing: 1.2px; }

/* SUMMARY */
.summary { padding: 26px; border-radius: 21px; background: linear-gradient(135deg, rgba(124,92,255,0.11), rgba(255,255,255,0.02)); border: 1px solid rgba(124,92,255,0.17); }
.summary-label { color: #9787ff; font-size: 9px; font-weight: 700; letter-spacing: 1.7px; }
.summary-text { margin-top: 10px; color: #d1d2d8; font-size: 14px; line-height: 1.85; }

/* TOPICS */
.topics { display: flex; flex-wrap: wrap; gap: 8px; }
.topic { padding: 8px 13px; border-radius: 999px; background: rgba(124,92,255,0.08); border: 1px solid rgba(124,92,255,0.16); color: #a79aff; font-size: 10px; }

/* DOCUMENT CARD */
.document-card { padding: 18px; border-radius: 18px; background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.07); }
.document-card-icon { width: 35px; height: 35px; display: flex; align-items: center; justify-content: center; border-radius: 10px; background: rgba(124,92,255,0.1); color: #a294ff; font-size: 9px; font-weight: 800; margin-bottom: 12px; }
.document-card-name { color: #d9dae0; font-size: 12px; font-weight: 600; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.document-card-meta { margin-top: 5px; color: #676b76; font-size: 10px; }

/* ANSWER */
.answer-header { padding: 10px 0 30px; }
.answer-title { margin-top: 7px; color: #f1f1f4; font-size: clamp(38px, 5vw, 58px); font-weight: 800; letter-spacing: -3px; }
.answer-subtitle { margin-top: 8px; color: #747883; font-size: 13px; }
.question-card { max-width: 920px; margin: 15px auto; padding: 19px 21px; border-radius: 17px; background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07); }
.question-label { color: #686c77; font-size: 8px; font-weight: 700; letter-spacing: 1.6px; }
.question-text { margin-top: 8px; color: #dedfe4; font-size: 14px; line-height: 1.65; }
.answer-card { max-width: 920px; margin: 0 auto 30px; padding: 27px; border-radius: 21px; background: linear-gradient(145deg, rgba(124,92,255,0.1), rgba(255,255,255,0.02)); border: 1px solid rgba(124,92,255,0.17); box-shadow: 0 30px 80px rgba(0,0,0,0.25); }
.answer-label { display: flex; align-items: center; gap: 8px; color: #9a89ff; font-size: 9px; font-weight: 700; letter-spacing: 1.7px; }
.answer-dot { width: 7px; height: 7px; border-radius: 50%; background: #63e6a7; box-shadow: 0 0 12px rgba(99,230,167,0.7); }
.answer-text { margin-top: 18px; color: #dedfe4; font-size: 14px; line-height: 1.9; }

/* EVIDENCE */
.evidence-title { max-width: 920px; margin: 0 auto; color: #6c707b; font-size: 9px; font-weight: 700; letter-spacing: 1.7px; }
.evidence-subtitle { max-width: 920px; margin: 5px auto 12px; color: #555a65; font-size: 11px; }
.source-card { max-width: 920px; margin: 9px auto; padding: 16px 18px; border-radius: 15px; background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07); }
.source-label { color: #676b76; font-size: 8px; font-weight: 700; letter-spacing: 1.5px; }
.source-file { margin-top: 7px; color: #d4d5da; font-size: 12px; }
.source-page { margin-top: 4px; color: #9687ff; font-size: 10px; }
.excerpt { padding: 17px; border-radius: 13px; background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); color: #c2c4cc; font-size: 12px; line-height: 1.8; }

/* STREAMLIT WIDGETS */
.stButton > button { min-height: 44px !important; border-radius: 13px !important; background: rgba(255,255,255,0.035) !important; border: 1px solid rgba(255,255,255,0.08) !important; color: #dedfe4 !important; font-weight: 600 !important; transition: 0.2s ease !important; }
.stButton > button:hover { background: rgba(124,92,255,0.11) !important; border-color: rgba(124,92,255,0.4) !important; color: white !important; transform: translateY(-1px); }
[data-testid="stFileUploader"] { max-width: 850px; margin: 0 auto; }
[data-testid="stFileUploaderDropzone"] { min-height: 140px !important; border: 1px dashed rgba(124,92,255,0.35) !important; border-radius: 18px !important; background: rgba(255,255,255,0.018) !important; }
[data-testid="stChatInput"] { max-width: 920px; margin-left: auto; margin-right: auto; }
[data-testid="stChatInput"] textarea { background: rgba(255,255,255,0.035) !important; color: white !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 16px !important; }

/* MOBILE */
@media (max-width: 700px) {
    .block-container { padding-left: 14px; padding-right: 14px; }
    .dm-online { display: none; }
    .welcome-brand { font-size: 57px; letter-spacing: -5px; }
    .welcome-tagline { font-size: 25px; }
    .welcome-description { max-width: 320px; font-size: 12px; }
    .welcome-flow { font-size: 7px; }
    .hero-title { font-size: 43px; letter-spacing: -2.5px; }
    .answer-card { padding: 21px; }
}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# NAVIGATION
# =========================================================

def render_nav():
    render_html("""
        <div class="dm-nav">
            <div class="dm-brand">
                <div class="dm-logo">✦</div>
                <div>
                    <div class="dm-brand-name">DOCUMIND</div>
                    <div class="dm-brand-subtitle">AI DOCUMENT INTELLIGENCE</div>
                </div>
            </div>
            <div class="dm-online">
                <span class="dm-online-dot"></span>
                AI ENGINE ONLINE
            </div>
        </div>
    """)


# =========================================================
# WELCOME
# =========================================================

def render_welcome():
    render_html("""
        <div class="welcome-wrapper">
            <div class="welcome-glow"></div>
            <div class="welcome-symbol">✦</div>
            <div class="welcome-brand">DOCUMIND</div>
            <div class="welcome-tagline">Your documents. Understood.</div>
            <div class="welcome-description">
                Turn complex documents into clear, grounded answers with AI.
            </div>
            <div class="welcome-flow">
                READ <span>→</span> UNDERSTAND <span>→</span> ASK <span>→</span> DISCOVER
            </div>
        </div>
    """)


# =========================================================
# HERO
# =========================================================

def render_hero():
    render_html("""
        <div class="hero">
            <div class="eyebrow">INTELLIGENT DOCUMENT UNDERSTANDING</div>
            <div class="hero-title">Ask your documents<br>anything.</div>
            <div class="hero-description">
                Upload your documents and let DocuMind transform complex
                information into clear, source-grounded answers.
            </div>
        </div>
    """)


# =========================================================
# UPLOAD HEADER
# =========================================================

def render_upload_header():
    render_html("""
        <div class="upload-card">
            <div class="upload-icon">↑</div>
            <div class="upload-title">Bring your document to life</div>
            <div class="upload-subtitle">Upload one or multiple PDF documents to begin.</div>
        </div>
    """)


# =========================================================
# PROCESSING
# =========================================================

def render_processing(title, subtitle):
    render_html(f"""
        <div class="processing">
            <div class="processing-orb"></div>
            <div class="processing-title">{html.escape(str(title))}</div>
            <div class="processing-subtitle">{html.escape(str(subtitle))}</div>
        </div>
    """)


# =========================================================
# UNDERSTOOD
# =========================================================

def render_understood():
    render_html("""
        <div class="success">
            <div class="success-icon">✓</div>
            <div class="success-title">I've understood your documents.</div>
            <div class="success-description">Your document knowledge base is ready.</div>
        </div>
    """)


# =========================================================
# STAT
# =========================================================

def render_stat(value, label):
    render_html(f"""
        <div class="stat">
            <div class="stat-value">{html.escape(str(value))}</div>
            <div class="stat-label">{html.escape(str(label))}</div>
        </div>
    """)


# =========================================================
# DOCUMENT CARD
# =========================================================

def render_document(name, pages):
    render_html(f"""
        <div class="document-card">
            <div class="document-card-icon">PDF</div>
            <div class="document-card-name">{html.escape(str(name))}</div>
            <div class="document-card-meta">{html.escape(str(pages))} pages · Ready</div>
        </div>
    """)


# =========================================================
# SOURCE
# =========================================================

def render_source(document, page):
    render_html(f"""
        <div class="source-card">
            <div class="source-label">SOURCE DOCUMENT</div>
            <div class="source-file">📄 {html.escape(str(document))}</div>
            <div class="source-page">Page {html.escape(str(page))}</div>
        </div>
    """)