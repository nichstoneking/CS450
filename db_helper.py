import os

import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

DB_PATH = "./chromadb"
COLLECTION_NAME = "slides"

PDF_PATHS = [
    "slides/01FoundationsAI.pdf",
    "slides/02Search.pdf",
    "slides/03ConstraintSatisfaction.pdf",
    "slides/04Learning.pdf",
    "slides/05NeuralNetworks.pdf",
    "slides/06DeepLearning.pdf",
    "slides/07LogicalAgents.pdf",
    "slides/08Uncertainty.pdf",
    "slides/09NaturalLanguageModels.pdf",
]

splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=150)


def load_pdf(collection, file_path):
    """Read a PDF and add page-level chunks with (source, page, chunk) metadata."""
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if not text:
                continue
            chunks = splitter.split_text(text)
            for j, chunk in enumerate(chunks):
                collection.add(
                    documents=[chunk],
                    metadatas=[{"source": file_name, "page": i, "chunk": j}],
                    ids=[f"{file_name}_page_{i}_chunk_{j}"],
                )
    print(f"Loaded {file_path}")


def rebuild():
    """Rebuild the slides collection from scratch so metadata stays consistent."""
    client = chromadb.PersistentClient(path=DB_PATH)

    # Drop any existing collection so re-runs don't duplicate or mix schemas.
    if any(c.name == COLLECTION_NAME for c in client.list_collections()):
        client.delete_collection(COLLECTION_NAME)

    collection = client.create_collection(name=COLLECTION_NAME)

    for pdf_path in PDF_PATHS:
        if os.path.exists(pdf_path):
            load_pdf(collection, pdf_path)
        else:
            print(f"File not found: {pdf_path}")

    print(f"Total documents (pages) in database: {collection.count()}")


if __name__ == "__main__":
    rebuild()