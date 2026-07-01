import os
import tempfile

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agents.graph import run_agent_pipeline
from src.rag.document_loader import load_and_split
from src.rag.vector_store import create_vector_store

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = None


class QueryRequest(BaseModel):
    query: str


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global vector_store

    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        chunks = load_and_split(tmp_path)
        if vector_store is None:
            vector_store = create_vector_store(chunks)
        else:
            vector_store.add_documents(chunks)
    finally:
        os.remove(tmp_path)

    return {"chunks_loaded": len(chunks)}


@app.post("/query")
async def query(request: QueryRequest):
    if vector_store is None:
        raise HTTPException(status_code=400, detail="No documents loaded. Upload a PDF first.")

    result = run_agent_pipeline(request.query, vector_store)

    return {
        "retrieved_docs": result["retrieved_docs"],
        "analysis": result["analysis"],
        "final_report": result["final_report"],
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "documents_loaded": vector_store is not None}


if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)