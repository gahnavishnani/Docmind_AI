# app.py

import html
import traceback

import streamlit as st
from dotenv import load_dotenv


# =========================================================
# CONFIG
# =========================================================

load_dotenv()

st.set_page_config(
    page_title="DocuMind AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# =========================================================
# UI IMPORT
# =========================================================

from ui import (
    inject_css,
    render_html,
    safe_text,
    render_nav,
    render_welcome,
    render_hero,
    render_upload_header,
    render_processing,
    render_understood,
    render_stat,
    render_document,
    render_source,
)

inject_css()


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "pipeline" not in st.session_state:
    st.session_state.pipeline = None

if "documents" not in st.session_state:
    st.session_state.documents = []

if "document_analysis" not in st.session_state:
    st.session_state.document_analysis = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# PAGE 1 — WELCOME
# =========================================================

if st.session_state.page == "welcome":

    render_welcome()

    render_html("""
        <div style="text-align:center; color:#747883; font-size:12px; margin-top:-20px; margin-bottom:22px;">
            AI-powered document intelligence
        </div>
    """)

    _, center, _ = st.columns([1, 1, 1])

    with center:
        if st.button(
            "Enter DocuMind  →",
            use_container_width=True,
            key="enter_documind",
        ):
            st.session_state.page = "workspace"
            st.rerun()

    st.stop()


# =========================================================
# PAGE 2 — WORKSPACE
# =========================================================

if st.session_state.page == "workspace":

    render_nav()

    # Heavy RAG packages are imported only here (not on the welcome page)
    from document_loader import extract_documents
    from rag_pipeline import RAGPipeline

    # =====================================================
    # EMPTY WORKSPACE (upload)
    # =====================================================

    if st.session_state.pipeline is None:

        render_hero()
        render_upload_header()

        uploaded_files = st.file_uploader(
            "Upload PDF documents",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
            key="pdf_upload",
        )

        if not uploaded_files:
            render_html("""
                <div style="text-align:center; padding:25px; color:#6e727d; font-size:12px;">
                    Drop your PDF above to begin.
                </div>
            """)
            st.stop()

        render_html("""
            <div class="section-label">SELECTED DOCUMENTS</div>
        """)

        for uploaded_file in uploaded_files:
            render_html(f"""
                <div class="document-row">
                    <div class="pdf-icon">PDF</div>
                    <div class="document-info">
                        <div class="document-name">{html.escape(uploaded_file.name)}</div>
                        <div class="document-meta">Ready to analyze</div>
                    </div>
                    <div class="document-check">✓</div>
                </div>
            """)

        st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

        if st.button(
            "✦  Understand my documents",
            use_container_width=True,
            key="understand_documents",
        ):
            # One placeholder so the processing cards replace each other
            status = st.empty()

            try:
                # STEP 1
                with status.container():
                    render_processing(
                        "Reading your documents",
                        "Extracting text from every page.",
                    )

                all_documents = []
                for uploaded_file in uploaded_files:
                    all_documents.extend(extract_documents(uploaded_file))

                if not all_documents:
                    status.empty()
                    st.error("No readable text was found in the uploaded PDF.")
                    st.stop()

                # STEP 2
                with status.container():
                    render_processing(
                        "Building document knowledge",
                        "Creating semantic representations for search.",
                    )

                pipeline = RAGPipeline()
                pipeline.process_documents(all_documents)

                # STEP 3
                with status.container():
                    render_processing(
                        "Understanding your document",
                        "Generating your summary and suggested questions.",
                    )

                analysis = pipeline.analyze_document()

                # SAVE
                st.session_state.pipeline = pipeline
                st.session_state.documents = all_documents
                st.session_state.document_analysis = analysis
                st.session_state.messages = []

                st.rerun()

            except Exception as error:
                status.empty()
                st.error("DocuMind could not process the document.")
                st.exception(error)
                with st.expander("Technical details"):
                    st.code(traceback.format_exc())
                st.stop()

        st.stop()

    # =====================================================
    # PROCESSED WORKSPACE
    # =====================================================

    render_understood()

    analysis = st.session_state.document_analysis or {}
    documents = st.session_state.documents

    # ---------------- STATS ----------------

    unique_documents = {item["document"] for item in documents}
    unique_pages = {(item["document"], item["page"]) for item in documents}
    chunk_count = len(st.session_state.pipeline.vector_store.chunks)

    render_html("""
        <div class="section-label">DOCUMENT INTELLIGENCE</div>
    """)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_stat(len(unique_documents), "Documents")
    with col2:
        render_stat(len(unique_pages), "Pages")
    with col3:
        render_stat(chunk_count, "Knowledge chunks")
    with col4:
        render_stat("READY", "AI status")

    # ---------------- SUMMARY ----------------

    render_html("""
        <div class="section-label">DOCUMENT OVERVIEW</div>
    """)

    summary = analysis.get(
        "summary",
        "Your document has been processed and is ready to explore.",
    )

    render_html(f"""
        <div class="summary">
            <div class="summary-label">AI SUMMARY</div>
            <div class="summary-text">{safe_text(summary)}</div>
        </div>
    """)

    # ---------------- TOPICS ----------------

    topics = analysis.get("topics", [])

    if topics:
        render_html("""
            <div class="section-label">KEY TOPICS</div>
        """)

        topic_html = "".join(
            f'<span class="topic">{html.escape(str(topic))}</span>'
            for topic in topics
        )

        render_html(f"""
            <div class="topics">{topic_html}</div>
        """)

    # ---------------- DOCUMENTS ----------------

    render_html("""
        <div class="section-label">YOUR DOCUMENTS</div>
    """)

    document_pages = {}
    for item in documents:
        document_pages.setdefault(item["document"], set()).add(item["page"])

    doc_columns = st.columns(min(3, len(document_pages)))

    for index, (name, pages) in enumerate(document_pages.items()):
        with doc_columns[index % len(doc_columns)]:
            render_document(name, len(pages))

    # ---------------- SUGGESTED QUESTIONS ----------------

    questions = analysis.get("questions", [])

    render_html("""
        <div class="section-label">EXPLORE YOUR DOCUMENT</div>
        <div style="color:#777b86; font-size:12px; margin-bottom:15px;">
            Ask one of these questions or write your own.
        </div>
    """)

    question_columns = st.columns(2)

    for index, question in enumerate(questions[:4]):
        with question_columns[index % 2]:
            if st.button(
                question,
                key=f"suggested_{index}",
                use_container_width=True,
            ):
                try:
                    result = st.session_state.pipeline.answer(question)

                    st.session_state.messages.append(
                        {"question": question, "result": result}
                    )
                    st.session_state.page = "answer"
                    st.rerun()

                except Exception as error:
                    st.error(f"Could not answer the question: {error}")

    # ---------------- CUSTOM QUESTION ----------------

    render_html("""
        <div style="text-align:center; padding:35px 0 10px; border-top:1px solid rgba(255,255,255,0.06); margin-top:35px;">
            <div class="eyebrow">ASK YOUR DOCUMENT</div>
            <div style="color:#eeeef1; font-size:26px; font-weight:600; margin-top:8px;">
                What would you like to know?
            </div>
            <div style="color:#70747f; font-size:11px; margin-top:6px;">
                Answers are generated only from your uploaded documents.
            </div>
        </div>
    """)

    custom_question = st.chat_input("Ask anything about your documents...")

    if custom_question:
        try:
            result = st.session_state.pipeline.answer(custom_question)

            st.session_state.messages.append(
                {"question": custom_question, "result": result}
            )
            st.session_state.page = "answer"
            st.rerun()

        except Exception as error:
            st.error(f"Could not answer the question: {error}")

    st.stop()


# =========================================================
# PAGE 3 — ANSWER
# =========================================================

if st.session_state.page == "answer":

    render_nav()

    if st.button("← Back to workspace", key="back_workspace"):
        st.session_state.page = "workspace"
        st.rerun()

    render_html("""
        <div class="answer-header">
            <div class="eyebrow">DOCUMENT INTELLIGENCE</div>
            <div class="answer-title">Grounded answer.</div>
            <div class="answer-subtitle">Your answer is grounded in your uploaded document.</div>
        </div>
    """)

    # ---------------- MESSAGES ----------------

    for message_index, message in enumerate(st.session_state.messages):

        question = message["question"]
        result = message["result"]

        # QUESTION
        render_html(f"""
            <div class="question-card">
                <div class="question-label">YOUR QUESTION</div>
                <div class="question-text">{safe_text(question)}</div>
            </div>
        """)

        # ANSWER
        answer = result.get(
            "answer",
            "I couldn't find this information in the uploaded documents.",
        )

        render_html(f"""
            <div class="answer-card">
                <div class="answer-label">
                    <span class="answer-dot"></span>
                    DOCUMIND ANSWER
                </div>
                <div class="answer-text">{safe_text(answer)}</div>
            </div>
        """)

        # SOURCES
        sources = result.get("sources", [])

        if sources:
            render_html("""
                <div class="evidence-title">EVIDENCE</div>
                <div class="evidence-subtitle">Retrieved passages used to ground this answer.</div>
            """)

            seen_sources = set()

            for index, source in enumerate(sources):

                key = (source.get("document"), source.get("page"))

                if key in seen_sources:
                    continue
                seen_sources.add(key)

                render_source(
                    source.get("document", "Unknown document"),
                    source.get("page", "Unknown"),
                )

                with st.expander(
                    f"View evidence · Page {source.get('page', 'Unknown')}",
                    expanded=(index == 0 and message_index == len(st.session_state.messages) - 1),
                ):
                    render_html(f"""
                        <div class="excerpt">{safe_text(source.get("text", ""))}</div>
                    """)

                    st.caption(
                        f"Semantic retrieval score: {source.get('score', 0):.3f}"
                    )

    # ---------------- FOLLOW UP ----------------

    render_html("""
        <div style="max-width:920px; margin:45px auto 0;">
            <div class="section-label">ASK A FOLLOW-UP</div>
        </div>
    """)

    follow_up = st.chat_input("Ask a follow-up question...")

    if follow_up:
        try:
            result = st.session_state.pipeline.answer(follow_up)

            st.session_state.messages.append(
                {"question": follow_up, "result": result}
            )
            st.rerun()

        except Exception as error:
            st.error(f"Could not answer the question: {error}")

    st.stop()