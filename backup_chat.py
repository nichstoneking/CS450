from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from transformers import logging as hf_logging

def chat():
    """Backup chat interface if langrepl isn't working"""
    hf_logging.set_verbosity_error()

    # Retrieve data from ChromaDB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    # Initialize LLM
    llm = OllamaLLM(model="qwen2.5:3b")

    # Create prompt template for and guidelines
    template = """You are a CS 450 (Introduction to Artificial Intelligence) Teaching Assistant.
    Guidelines:
    Give clear, accurate explanations tailored to an undergraduate computer science audience.
    When appropriate, use examples, analogies, or step-by-step breakdowns to aid understanding.
    If a question is ambiguous, ask clarifying questions before answering.
    If you are unsure based on the context, mention it is not in the context.
    Be concise in your explanations.
    Use the following context to answer the question.
    
    Context:
    {context}
    
    Question: {input}
    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("CS 450 Teaching Assistant\nType exit to quit.\n")

    # Chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        print("\nCS 450 Assistant: ", end="", flush=True)   # Print words one by one
        for chunk in chain.stream(user_input):
            print(chunk, end="", flush=True)    # Print words one by one
        print("\n")

if __name__ == "__main__":
    chat()