import uuid
from io import BytesIO
from typing import List
from pypdf import PdfReader

from app.embeddings import model
from app.vector_client import qdrant, create_collection
from app.config import COLLECTION_NAME


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start = end - overlap
    return chunks


def ingest_pdf(pdf_bytes: bytes, filename: str, source_url: str | None = None) -> int:
    """
    Extracts text, chunks it, embeds it, and pushes to Qdrant.
    Stores source_url in metadata if provided.
    """
    reader = PdfReader(BytesIO(pdf_bytes))

    vector_size = model.get_sentence_embedding_dimension()
    create_collection(vector_size)

    points = []

    for page_idx, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        cleaned = " ".join(raw_text.split())
        if not cleaned:
            continue

        chunks = chunk_text(cleaned)

        for chunk_idx, chunk in enumerate(chunks):
            emb = model.encode(chunk).tolist()

            points.append({
                "id": str(uuid.uuid4()),
                "vector": emb,
                "payload": {
                    "title": filename,
                    "source_type": "pdf",
                    "text": chunk,
                    "pdf_name": filename,
                    "page": page_idx + 1,
                    "chunk_index": chunk_idx,
                    "url": source_url  # 👈 storing metadata here
                }
            })

    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)
