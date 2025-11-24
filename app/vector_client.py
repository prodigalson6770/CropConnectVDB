from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, SearchParams
from app.config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME

qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def create_collection(vector_size: int):
    existing = [c.name for c in qdrant.get_collections().collections]

    if COLLECTION_NAME not in existing:
        print(f"📁 Creating new Qdrant collection: {COLLECTION_NAME}")
        qdrant.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


def search_vectors(vector: list[float], top_k: int = 5):
    return qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=vector,
        limit=top_k,
        with_payload=True,
        search_params=SearchParams(hnsw_ef=128),
    )
