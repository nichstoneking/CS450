# Project Proposal — Fine Tuning

## Who
- Theo Leonard
- William Gray
- Nicholas Stoneking
- Duncan Hugelmaier

## What and Why

Run rag on an OS model for CS450, lecture slides and assignments embedded.

## How

**Model:** Qwen2.5 3B

**Tasks:**
- ~~Product definition~~
- ~~Figure out stack~~
- Diagram
- Implement

**Product Design Choices:**
- Text interface (maybe find cool cli library for this)
- Locally hosted model (?)
- Embedding pipeline
- Iterate if more time
  - agentic RAG? maybe we could include some of the code, other resources, etc

**Tech stack:**
- Python
- Langrepl (start with)
- Langchain (Qwen2.5 3B)
- ChromaDB (local)

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) (Python package manager)
- [Ollama](https://ollama.com/) with `qwen2.5:3b` pulled (`ollama pull qwen2.5:3b`)

### Install & Run

```bash
uv tool install langrepl        # install the CLI
ollama serve                     # start Ollama in a separate terminal
langrepl -w .                    # start chatting (cs450-tutor agent)
```

Switch models with the `-m` flag or interactively with `/model` (Enter on agent, then Tab between providers):

```bash
langrepl -w . -m gpt-mini       # start with GPT-4.1-mini (needs OpenAI key in .env)
langrepl -w . -m qwen-local     # start with Qwen2.5 3B (needs Ollama running)
```
