from typing import TypedDict


class RAGState(TypedDict):
    question: str
    documents: list
    answer: str
    route: str
    document_grade: str
    rewrite_count: int