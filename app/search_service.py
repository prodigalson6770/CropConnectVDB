from app.embeddings import model
from app.vector_client import search_vectors
from app.models import Match, Source

def retrieve_context(query_text: str, top_k: int):
    print("🔍 Embedding and searching for:", query_text)
    
    query_vec = model.encode(query_text).tolist()
    results = search_vectors(query_vec, top_k)

    matches = []
    for r in results:
        p = r.payload

        matches.append(Match(
            text=p["text"],
            source=Source(
                title=p.get("title", "Unknown"),
                source_type=p.get("source_type", "pdf"),
                pdf_name=p.get("pdf_name"),
                url=p.get("url"),
                page=p.get("page"),
            )
        ))

    return matches
