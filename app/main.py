from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

from app.pdf_ingest import ingest_pdf
from app.search_service import retrieve_context
from app.models import SearchRequest, SearchResponse

app = FastAPI(title="CropConnect RAG Backend (With URL Metadata)")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/upload_pdf")
async def upload_pdf(
    file: UploadFile = File(...),
    source_url: str = Form(None)  # 👈---- receives URL
):
    pdf_bytes = await file.read()
    chunks_added = ingest_pdf(pdf_bytes, file.filename, source_url)

    return {
        "status": "success",
        "file": file.filename,
        "chunks_added": chunks_added,
        "stored_url": source_url
    }


@app.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest):
    matches = retrieve_context(req.query_text, req.top_k)
    return SearchResponse(matches=matches)
