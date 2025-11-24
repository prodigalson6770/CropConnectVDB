from pydantic import BaseModel
from typing import List, Optional

class Source(BaseModel):
    title: str
    source_type: str
    url: Optional[str] = None
    pdf_name: Optional[str] = None
    page: Optional[int] = None


class SearchRequest(BaseModel):
    query_text: str
    top_k: int = 5


class Match(BaseModel):
    text: str
    source: Source


class SearchResponse(BaseModel):
    matches: List[Match]
