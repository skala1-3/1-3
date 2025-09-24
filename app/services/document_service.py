# documents_api.py
from fastapi import APIRouter, UploadFile
from app.services.document_service import save_document, parse_document
from app.services.chunk_service import chunk_text
from app.services.embedding_service import generate_embedding

router = APIRouter()

@router.post("/api/documents/upload")
async def upload_document(file: UploadFile):
    doc_id = save_document(file)
    return {"doc_id": str(doc_id)}

@router.post("/api/documents/{doc_id}/parse")
async def parse_doc(doc_id: str):
    text = parse_document(doc_id)
    return {"doc_id": doc_id, "length": len(text)}

@router.post("/api/documents/{doc_id}/chunk")
async def chunk_doc(doc_id: str):
    text = parse_document(doc_id)
    chunks = chunk_text(text)
    return {"doc_id": doc_id, "num_chunks": len(chunks)}

@router.post("/api/documents/{doc_id}/embed")
async def embed_doc(doc_id: str):
    text = parse_document(doc_id)
    chunks = chunk_text(text)
    embeddings = [generate_embedding(c) for c in chunks]
    return {"doc_id": doc_id, "num_embeddings": len(embeddings)}
