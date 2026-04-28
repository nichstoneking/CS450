from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from transformers import logging as hf_logging
from sentence_transformers import SentenceTransformer, util

#map of lecture filenames to descriptions for better retrieval context
LECTURE_DESCRIPTIONS = {
    "01FoundationsAI.pdf": "foundations of artificial intelligence, agents, rationality, environments",
    "02Search.pdf": "search algorithms, uninformed search, BFS, DFS, UCS, A star, heuristics",
    "03ConstraintSatisfaction.pdf": "constraint satisfaction problems, CSPs, variables, domains, constraints, backtracking",
    "04Learning.pdf": "machine learning basics, supervised learning, training data, features, labels",
    "05NeuralNetworks.pdf": "neural networks, perceptrons, activation functions, backpropagation, HuggingFace",
    "06DeepLearning.pdf": "deep learning, CNNs, convolution, pooling, computer vision",
    "07LogicalAgents.pdf": "logic, logical agents, propositional logic, inference, knowledge bases",
    "08Uncertainty.pdf": "uncertainty, probability, Bayes rule, Bayesian networks, decision making",
    "09NaturalLanguageModels.pdf": "natural language processing, NLP, language models, embeddings, RNNs, attention, transformers, LLMs"
}

def chat():
    """Backup chat interface if langrepl isn't working"""
    hf_logging.set_verbosity_error()

    # Retrieve data from ChromaDB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    router_model = SentenceTransformer("all-MiniLM-L6-v2")
    lecture_names = list(LECTURE_DESCRIPTIONS.keys())
    lecture_texts = list(LECTURE_DESCRIPTIONS.values())
    lecture_embeddings = router_model.encode(lecture_texts, convert_to_tensor=True)

    # Function to choose best source based on question embedding similarity
    def choose_best_source(question):
        question_embedding = router_model.encode(question, convert_to_tensor=True)
        scores = util.cos_sim(question_embedding, lecture_embeddings)[0]
        best_index = scores.argmax().item()
        best_source = lecture_names[best_index]
        best_score = scores[best_index].item()

        print(f"\nSelected source: {best_source} (score: {best_score:.3f})")

        return best_source
    
    vectorstore = Chroma(
        persist_directory="./chromadb",
        embedding_function=embeddings,
        collection_name="slides"
    )
    #retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    #debugging step to ensure model is retrieving from slides
    def format_docs(docs):
        print("\n--- Retrieved context from ChromaDB ---")
        formatted_docs = []
        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "unknown source")
            page = doc.metadata.get("page", "unknown page")
            chunk = doc.metadata.get("chunk", "unknown chunk")
            print(f"\n[Document {i}]")
            print(f"Source: {source}, page {page}, chunk {chunk}")
            print(doc.page_content[:500])
            print("...")
            formatted_docs.append(
                f"[Source: {source}, page {page}, chunk {chunk}]\n{doc.page_content}"
            )
        print("\n--- End retrieved context ---\n")
        return "\n\n".join(formatted_docs)

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
    Every paragraph that uses retrieved context MUST end with a citation in this exact format: (source: <filename>, page <number>, chunk <number>). Do not include uncited claims from the slides.
    Use the following context to answer the question.
    
    Context:
    {context}
    
    Question: {input}
    Answer:"""

    prompt = ChatPromptTemplate.from_template(template)

    

    print("CS 450 Teaching Assistant\nType exit to quit.\n")

    # Chat loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        selected_source = choose_best_source(user_input)
        retriever = vectorstore.as_retriever(
            search_kwargs={
                "k": 5,
                "filter": {"source": selected_source}
            }
        )

        chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
        )

        print("\nCS 450 Assistant: ", end="", flush=True)   # Print words one by one
        for chunk in chain.stream(user_input):
            print(chunk, end="", flush=True)    # Print words one by one
        print("\n")

if __name__ == "__main__":
    chat()