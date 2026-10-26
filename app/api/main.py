"""
RAG API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.rag.rag_service import RAGService


app = FastAPI(
    title="Knowledge Assistant API",
    description="A document-grounded question-answering API.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

rag_service = RAGService()

class QueryRequest(BaseModel):
    """
    Query Request Data Model
    """
    question: str

class QueryResponse(BaseModel):
    """
    Query Reponse Data Model
    """
    question: str
    answer: str
    sources: list[dict]

@app.get("/health")
def health():
    """
    Health endpoint
    """
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    """
    query endpoint
    """
    result = rag_service.query(request.question)

    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": result["sources"],
    }
