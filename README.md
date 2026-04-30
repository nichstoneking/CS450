# Project Proposal — Fine Tuning

## Who
- Theo Leonard
- William Gray
- Nicholas Stoneking
- Duncan Hugelmaier

## What and Why

Run RAG on an open-source model for CS 450, lecture slides embedded.

## How

**Model:** Qwen2.5 3B (local via Ollama) or GPT-4.1-mini (OpenAI) — switchable inside langREPL with `/model`.

**Tasks:**
- Product definition
- Figure out stack
- Diagram
- Implement

**Product Design Choices:**
- Text interface (langREPL)
- Locally hosted model option
- Embedding pipeline
- Iterate if more time

**Tech stack:**
- Python 3.14
- [langREPL](https://github.com/midodimori/langrepl) as the agent runtime
- [`chroma-mcp`](https://github.com/chroma-core/chroma-mcp) (Model Context Protocol server) exposing the local ChromaDB to the agent as tools
- ChromaDB (local persistent client) as the vector store

## Architecture

```
You ──► langrepl (cs450-tutor agent)
           │
           ├─ MCP stdio ──► uvx chroma-mcp (subprocess)
           │                     │
           │                     └─► ./chromadb (chroma.sqlite3 + HNSW)
           │
           └─ LLM call ──► Ollama qwen2.5:3b   (default in this repo)
                           or OpenAI gpt-4.1-mini
```

The agent decides at runtime when to call `chroma_query_documents` against the
`slides` collection, filters by lecture via `where: {"source": "<filename>.pdf"}`,
and cites retrieved chunks back to the user.

## Getting Started

### Prerequisites

- Python 3.14 or newer
- [`uv`](https://docs.astral.sh/uv/) (used both for project deps and to run `chroma-mcp` on demand)
- [`langrepl`](https://github.com/midodimori/langrepl) installed (e.g. `uv tool install langrepl`)
- One of:
  - `ollama` running locally with `qwen2.5:3b` pulled (`ollama pull qwen2.5:3b`), **or**
  - an OpenAI API key in `.env` as `LLM__OPENAI_API_KEY=...`

### Install

```bash
uv sync                          # installs project deps into .venv (only needed for db_helper.py / backup_chat.py)
```

### Add the slides

The lecture PDFs are not included in this repo. Download them from Canvas
and drop them into the `slides/` folder. The default `PDF_PATHS` list in
[`db_helper.py`](db_helper.py) expects these filenames:

```
slides/01FoundationsAI.pdf
slides/02Search.pdf
slides/03ConstraintSatisfaction.pdf
slides/04Learning.pdf
slides/05NeuralNetworks.pdf
slides/06DeepLearning.pdf
slides/07LogicalAgents.pdf
slides/08Uncertainty.pdf
slides/09NaturalLanguageModels.pdf
```

If your filenames differ, rename them or edit `PDF_PATHS` in `db_helper.py`
to match. The filename is what the agent will cite back as `source`, so use
clean names.

### Build the embeddings

Once the PDFs are in `slides/`, build (or rebuild) the local ChromaDB store:

```bash
rm -rf chromadb              # only needed if a previous store exists
.venv/bin/python db_helper.py    # ~5–10 min on CPU for the 9 default decks
```

`db_helper.py` is idempotent — it deletes and recreates the `slides`
collection on every run, so re-running it will never duplicate chunks.

### Run

```bash
ollama serve                     # only if using qwen-local; in another terminal
langrepl                         # from the project root
```

langREPL auto-loads `.langrepl/` and starts the `cs450-tutor` agent. Inside the
prompt:

- Ask CS 450 questions normally — the agent retrieves relevant slide chunks
  before answering and cites `(source: <filename>, page <n>, chunk <m>)`.
- `/model` to switch between `qwen-local` and `gpt-mini`.
- `/tools` should list five `chroma_*` tools sourced from the `chroma` MCP server.

### Fallback chat (without langREPL)

If langREPL is unavailable, the original LangChain-based chat still works:

```bash
.venv/bin/python backup_chat.py
```

## Files of note

- `.langrepl/config.mcp.json` — registers the `chroma` MCP server (stdio,
  `uvx chroma-mcp --client-type persistent --data-dir ./chromadb`).
- `.langrepl/agents/cs450-tutor.yml` — exposes the read-only `chroma_*` tools
  to the tutor agent via `tools.patterns`.
- `.langrepl/prompts/agents/cs450_tutor.md` — system prompt with the lecture
  filename map and the required retrieval / citation workflow.
- `db_helper.py` — re-embeds the slides into `./chromadb` with `source`/`page`/`chunk`
  metadata.
- `backup_chat.py` — standalone LangChain fallback chat.
