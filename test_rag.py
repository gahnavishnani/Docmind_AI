import os

from dotenv import load_dotenv

from document_loader import extract_documents
from rag_pipeline import RAGPipeline


load_dotenv()


class FakePDF:
    def __init__(self, path):
        self.name = os.path.basename(path)

        with open(path, "rb") as f:
            self.data = f.read()

    def getvalue(self):
        return self.data


pdf = FakePDF("documents/sample.pdf")

documents = extract_documents(pdf)

print(f"Pages extracted: {len(documents)}")

pipeline = RAGPipeline()

pipeline.process_documents(documents)

print("Vector store created successfully.")

result = pipeline.answer(
    "What is this document about?"
)

print("\nANSWER:")
print(result["answer"])

print("\nSOURCES:")

for source in result["sources"]:
    print(
        f"- {source['document']} | "
        f"Page {source['page']} | "
        f"Score {source['score']:.3f}"
    )