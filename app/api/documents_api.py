# app/api/documents_api.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.db_models import Document
from app.db import get_db
import uuid

router = APIRouter()

@router.post("/api/documents/create")
def create_document(title: str, doc_type: str, db: Session = Depends(get_db)):
    doc = Document(
        doc_id=uuid.uuid4(),
        title=title,
        doc_type=doc_type
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return {"doc_id": str(doc.doc_id), "title": doc.title, "doc_type": doc.doc_type}

@router.get("/api/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return docs
