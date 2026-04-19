import chromadb
from pypdf import PdfReader
import os

# Setup database file
client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection(name="slides")

def load_pdf(file_path):
    """Load a PDF file and extract text content"""
    reader = PdfReader(file_path)
    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            collection.add(
                documents=[text],
                ids=[f"page_{i}"]
            )
    print(f"Loaded {file_path}")

if __name__ == "__main__":
    pdf_path = "slides/01FoundationsAI.pdf" # Replace with PDF file path you want to load
    if os.path.exists(pdf_path):
        load_pdf(pdf_path)
    else:
        print(f"File not found: {pdf_path}")