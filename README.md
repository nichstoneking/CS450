# Project Proposal — Fine Tuning

## Who
- Theo Leonard
- William Gray
- Nicholas Stoneking
- Duncan Hugelmaier

## What and Why

Run rag on an OS model for CS450, lecture slides embedded.

## How

**Model:** Qwen2.5 3B

**Tasks:**
- Product definition
- Figure out stack
- Diagram
- Implement

**Product Design Choices:**
- Text interface
- Locally hosted model
- Embedding pipeline
- Iterate if more time
  - agentic RAG? maybe we could include some of the code, other resources, etc

**Tech stack:**
- Python
- Local Python scripts for RAG and ChromaDB
- Langchain (Qwen2.5 3B)
- ChromaDB (local)

## Getting Started

### Prerequisites

- Python 3.14 or newer
- `ollama` installed and running locally
- `qwen2.5:3b` pulled in Ollama (`ollama pull qwen2.5:3b`)

### Install & Run

```bash
ollama serve                     # start Ollama in a separate terminal
python backup_chat.py            # start chat
```

> Note: Project proceeded without using `langrepl` for RAG. The current workflow is based on local Python scripts (`db_helper.py`, `backup_chat.py`) and local Ollama model access.

If you want to switch to GPT, switch llm in `backup_chat.py`:

```bash
llm = ChatOpenAI(model="choose model here", api_key="your api key here")
```

If you want to regenerate slide embeddings, uncomment and run:

```bash
python db_helper.py
```
