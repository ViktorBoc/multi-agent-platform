# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

This repository is currently an empty scaffold (only `.idea/`, `.venv`, `.env`, `.gitignore` exist — no source code yet). The architecture and structure below is the **planned** design agreed with the user; nothing is implemented yet. Update this file as each phase lands so it stays accurate.

## Purpose

Multi-Agent Research Platform: a user uploads PDF documents and asks a question. Three LLM agents collaborate to answer it:

1. **Retrieval Agent** — runs the RAG pipeline, fetches relevant chunks from the vector store.
2. **Analysis Agent** — analyzes the retrieved passages via LLM.
3. **Synthesis Agent** — generates the final structured report with citations.

## Build order (phased)

Build and validate in this order — don't jump ahead:

1. RAG pipeline (`src/rag/`: PDF loading/chunking, embeddings, Chroma vector store, similarity search)
2. Agents (`src/agents/`: shared state, the three agent nodes, LangGraph `StateGraph` wiring them together)
3. API (`src/api/`: FastAPI endpoints that invoke the graph)
4. Frontend (`src/frontend/`: Streamlit upload + chat UI calling the API)
5. Docker (Dockerfiles + `docker-compose.yml` wiring api, frontend, chromadb services)
6. Deploy (Streamlit Cloud, live demo link)

## Planned architecture

```
Streamlit frontend (PDF upload, chat UI)
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
PDF → chunking → OpenAI embeddings (text-embedding-3-small) → ChromaDB → similarity search
```

Agent state is shared via a `TypedDict` (`src/agents/state.py`) passed through the LangGraph nodes — retrieval output feeds analysis, analysis output feeds synthesis.

## Planned directory structure

```
src/
  rag/
    document_loader.py   # PDF loading + chunking
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
```

## Tech stack

- Python 3.11+
- LangChain + LangGraph — agents, RAG, orchestration
- ChromaDB — vector store
- OpenAI API — embeddings: `text-embedding-3-small`; LLM: `gpt-4o-mini`
- FastAPI + uvicorn — backend API
- Streamlit — frontend
- Docker + Docker Compose — containerization; services: `api`, `frontend`, `chromadb`
- Deploy target: Streamlit Cloud

## Environment

- `OPENAI_API_KEY` is read from `.env` (gitignored — never commit it).
- `.chroma/` (local Chroma persistence dir) is also gitignored.

## Commands

Not yet applicable — no `requirements.txt`, entrypoints, or tests exist yet. Once the corresponding phase lands, this section should be filled in with the real commands, e.g. dependency install, `uvicorn src.api.main:app --reload`, `streamlit run src/frontend/app.py`, `docker-compose up`, and the test runner.

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