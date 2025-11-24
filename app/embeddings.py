from sentence_transformers import SentenceTransformer
from app.config import EMBEDDING_MODEL

print("🧠 Loading embedding model:", EMBEDDING_MODEL)
model = SentenceTransformer(EMBEDDING_MODEL)
