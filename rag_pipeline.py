import os
from typing import Dict, List

from groq import Groq

from prompt import SYSTEM_PROMPT
from vector_store import DocumentVectorStore


class RAGPipeline:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(api_key=api_key)

        self.vector_store = DocumentVectorStore()

    def process_documents(self, documents: List[Dict]):
        """
        Build the vector store from extracted documents.
        """

        self.vector_store.build(documents)

    def retrieve(
        self,
        question: str,
        top_k: int = 4,
    ) -> List[Dict]:

        return self.vector_store.search(
            question,
            top_k=top_k,
        )

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

        for i, chunk in enumerate(retrieved_chunks, start=1):

            context_parts.append(
                f"""
SOURCE {i}
Document: {chunk['document']}
Page: {chunk['page']}

Content:
{chunk['text']}
"""
            )

        context = "\n".join(context_parts)

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

        answer = response.choices[0].message.content.strip()

        return {
            "answer": answer,
            "sources": retrieved_chunks,
        }