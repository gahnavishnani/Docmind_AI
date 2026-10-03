from typing import List, Dict, Tuple

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentVectorStore:
    def __init__(self):
        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=120,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

        self.index = None
        self.chunks = []

    def build(self, documents: List[Dict]):
        """
        Convert extracted documents into chunks,
        embeddings and a FAISS index.
        """

        self.chunks = []

        for document in documents:
            split_texts = self.text_splitter.split_text(
                document["text"]
            )

            for text in split_texts:
                self.chunks.append(
                    {
                        "text": text,
                        "document": document["document"],
                        "page": document["page"],
                    }
                )

        if not self.chunks:
            raise ValueError(
                "No readable text was found in the uploaded document."
            )

        texts = [chunk["text"] for chunk in self.chunks]

        embeddings = self.embedding_model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        embeddings = embeddings.astype("float32")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def search(
        self,
        query: str,
        top_k: int = 4,
    ) -> List[Dict]:
        """
        Retrieve the most relevant chunks for a question.
        """

        if self.index is None:
            raise ValueError("Vector store has not been built yet.")

        query_embedding = self.embedding_model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype("float32")

        scores, indices = self.index.search(
            query_embedding,
            min(top_k, len(self.chunks)),
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            chunk = self.chunks[index].copy()
            chunk["score"] = float(score)

            results.append(chunk)

        return results