# DocuMind AI

> **AI-Powered Domain-Specific RAG Chatbot for PDF Question Answering**

DocuMind AI is an AI-powered document intelligence application that allows users to upload PDF documents, understand their content, and ask questions using natural language.

It uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from uploaded documents and generate grounded answers based only on the retrieved document context, along with source document and page references.

**Live Demo:** [DocuMind AI](https://docmindai-echhgupx8hfcr57f7sw2bm.streamlit.app/)

---

## Features

- Upload one or multiple PDF documents
- Extract text page-by-page using `pypdf`
- Preserve document name and page metadata
- Split documents into overlapping chunks
- Generate semantic embeddings using Sentence Transformers
- Store and search embeddings using FAISS
- Retrieve the most relevant document chunks
- Generate grounded answers using Groq
- Display source document and page information
- Generate AI-powered document summaries
- Generate suggested questions from uploaded documents
- Context-only prompting to reduce hallucinations
- Refuse unsupported questions when information is not available
- Modern dark-themed Streamlit interface
- Deployed on Streamlit Community Cloud

---

## How It Works

DocuMind AI implements a complete Retrieval-Augmented Generation pipeline:

```text
┌─────────────────────┐
│     PDF Upload      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Text Extraction   │
│       (pypdf)       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Chunking       │
│   900 / 120 chars   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Embeddings      │
│ all-MiniLM-L6-v2    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    FAISS Index      │
└──────────┬──────────┘
           │
           │
      User Question
           │
           ▼
┌─────────────────────┐
│ Query Embedding     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Relevant Chunks     │
│     Retrieval       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Context + Question  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Groq LLM       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Grounded Answer +   │
│       Sources       │
└─────────────────────┘
