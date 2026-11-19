from pydantic import BaseModel


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
