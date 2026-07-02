# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

All phases below are implemented. Update this file as the architecture evolves so it stays accurate.

## Purpose

Multi-Agent Research Platform: a user uploads documents (PDF, Word, PowerPoint, Excel, HTML, CSV, JSON, XML, or images) and asks a question. Three LLM agents collaborate to answer it:

1. **Retrieval Agent** — runs the RAG pipeline, fetches relevant chunks from the vector store.
2. **Analysis Agent** — analyzes the retrieved passages via LLM.
3. **Synthesis Agent** — generates the final structured report with citations.

## Architecture

```
Streamlit frontend (document upload, chat UI)
        │  HTTP
        ▼
FastAPI backend (API layer)
        │  invokes
        ▼
LangGraph StateGraph — 3-agent pipeline
        │
        ├─ Retrieval Agent  → RAG pipeline (query → similarity search)
        ├─ Analysis Agent   → LLM analyzes retrieved chunks
        └─ Synthesis Agent  → LLM generates final report w/ citations

RAG pipeline (offline/ingest path):
document → MarkItDown (Markdown conversion) → chunking → OpenAI embeddings (text-embedding-3-small) → ChromaDB → similarity search
```

Agent state is shared via a `TypedDict` (`src/agents/state.py`) passed through the LangGraph nodes — retrieval output feeds analysis, analysis output feeds synthesis.

## Directory structure

```
src/
  rag/
    document_loader.py   # MarkItDown conversion + chunking (any supported format)
    vector_store.py       # ChromaDB + embeddings + retrieval
  agents/
    state.py              # shared TypedDict state
    retrieval_agent.py     # RAG retrieval node
    analysis_agent.py      # LLM analysis node
    synthesis_agent.py     # report generation node
    graph.py               # LangGraph StateGraph wiring
  api/
    main.py                # FastAPI endpoints
  frontend/
    app.py                 # Streamlit UI
docker/
  Dockerfile.api
  Dockerfile.frontend
docker-compose.yml
requirements.txt
streamlit_app.py           # standalone Streamlit Cloud version (no FastAPI backend)
```

## Tech stack

- Python 3.11+
- LangChain + LangGraph — agents, RAG, orchestration
- MarkItDown — converts PDF, Word, PowerPoint, Excel, HTML, CSV, JSON, XML, and images to Markdown before chunking; images are described via OpenAI vision (`gpt-4o-mini`)
- ChromaDB — vector store
- OpenAI API — embeddings: `text-embedding-3-small`; LLM + vision: `gpt-4o-mini`
- FastAPI + uvicorn — backend API
- Streamlit — frontend
- Docker + Docker Compose — containerization; services: `api`, `frontend`, `chromadb`
- Deploy target: Streamlit Cloud

## Supported upload formats

`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.csv`, `.json`, `.xml`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff` — enforced by `ALLOWED_EXTENSIONS` in `src/api/main.py`; the Streamlit uploaders (`src/frontend/app.py`, `streamlit_app.py`) restrict `type=` to the same list.

## Environment

- `OPENAI_API_KEY` is read from `.env` (gitignored — never commit it). Required for embeddings, chat completions, and MarkItDown's image vision calls.
- `.chroma/` (local Chroma persistence dir) is also gitignored.

## Commands

- Install deps: `pip install -r requirements.txt`
- Run API: `uvicorn src.api.main:app --reload`
- Run frontend: `streamlit run src/frontend/app.py`
- Run everything: `docker compose up --build`
- Run standalone Streamlit Cloud version: `streamlit run streamlit_app.py`

## Coding Guidelines (Karpathy)

1. Think Before Coding
Don't assume. Don't hide confusion. Surface tradeoffs.
Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

2. Simplicity First
Minimum code that solves the problem. Nothing speculative.
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

3. Surgical Changes
Touch only what you must. Clean up only your own mess.
When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

4. Goal-Driven Execution
Define success criteria. Loop until verified.
Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.