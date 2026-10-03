import json
import os
from typing import Dict, List

from groq import Groq

from prompt import (
    SYSTEM_PROMPT,
    DOCUMENT_ANALYSIS_PROMPT,
)

from vector_store import DocumentVectorStore


class RAGPipeline:

    def __init__(self):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.vector_store = DocumentVectorStore()

    # ========================================================
    # DOCUMENT PROCESSING
    # ========================================================

    def process_documents(
        self,
        documents: List[Dict],
    ):

        self.vector_store.build(
            documents
        )

    # ========================================================
    # RETRIEVAL
    # ========================================================

    def retrieve(
        self,
        question: str,
        top_k: int = 4,
    ) -> List[Dict]:

        return self.vector_store.search(
            question,
            top_k=top_k,
        )

    # ========================================================
    # DOCUMENT ANALYSIS
    # ========================================================

    def analyze_document(
        self,
        max_chunks: int = 12,
    ) -> Dict:

        chunks = self.vector_store.chunks

        if not chunks:
            return {
                "summary": "No document content was found.",
                "topics": [],
                "questions": [],
            }

        # Select representative chunks rather than
        # sending the entire document to the LLM.
        selected_chunks = chunks[:max_chunks]

        context_parts = []

        for chunk in selected_chunks:

            context_parts.append(
                f"""
Document: {chunk['document']}
Page: {chunk['page']}

Content:
{chunk['text']}
"""
            )

        context = "\n".join(
            context_parts
        )

        prompt = DOCUMENT_ANALYSIS_PROMPT.format(
            context=context
        )

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        raw_response = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        try:

            result = json.loads(
                raw_response
            )

        except json.JSONDecodeError:

            # Safe fallback if the model returns
            # slightly malformed JSON.

            result = {
                "summary": (
                    "Your document has been processed "
                    "and is ready to explore."
                ),
                "topics": [],
                "questions": [
                    "What are the key points?",
                    "Can you summarize this document?",
                    "What information is most important?",
                    "What should I know from this document?",
                ],
            }

        return {
            "summary": result.get(
                "summary",
                "Your document is ready to explore.",
            ),
            "topics": result.get(
                "topics",
                [],
            ),
            "questions": result.get(
                "questions",
                [],
            )[:4],
        }

    # ========================================================
    # QUESTION ANSWERING
    # ========================================================

    def answer(
        self,
        question: str,
        top_k: int = 4,
    ) -> Dict:

        retrieved_chunks = self.retrieve(
            question,
            top_k=top_k,
        )

        context_parts = []

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1,
        ):

            context_parts.append(
                f"""
SOURCE {index}
Document: {chunk['document']}
Page: {chunk['page']}

Content:
{chunk['text']}
"""
            )

        context = "\n".join(
            context_parts
        )

        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question,
        )

        response = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0,
        )

        answer = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return {
            "answer": answer,
            "sources": retrieved_chunks,
        }