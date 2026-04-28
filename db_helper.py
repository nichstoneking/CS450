import chromadb
import os
import PyPDF2
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Setup database file
client = chromadb.PersistentClient(path="./chromadb")
collection = client.get_or_create_collection(name="slides")

# Setup text splitter for chunking PDF content
splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=150
)

def load_pdf(file_path):
    """Load a PDF file and extract text content"""
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                chunks = splitter.split_text(text)
                for j, chunk in enumerate(chunks):
                    collection.add(
                        documents=[chunk],
                        metadatas=[{"source": file_name, "page": i, "chunk": j}],
                        ids=[f"{file_name}_page_{i}_chunk_{j}"]
                    )
    print(f"Loaded {file_path}")

# NOTE: This code block has already been executed to initialize ChromaDB with the PDF data.
# To reload the data, delete the chromadb folder and uncomment the code block below to run it again.
if __name__ == "__main__":
    """pdf_paths = ["slides/01FoundationsAI.pdf",
                 "slides/02Search.pdf",
                 "slides/03ConstraintSatisfaction.pdf",
                 "slides/04Learning.pdf",
                 "slides/05NeuralNetworks.pdf",
                 "slides/06DeepLearning.pdf",
                 "slides/07LogicalAgents.pdf",
                 "slides/08Uncertainty.pdf",
                 "slides/09NaturalLanguageModels.pdf"]
    for pdf_path in pdf_paths:
        if os.path.exists(pdf_path):
            load_pdf(pdf_path)
        else:
            print(f"File not found: {pdf_path}")"""
    
    # Test if data is in database
    print(f"Total documents (pages) in database: {collection.count()}")