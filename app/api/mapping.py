from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.core.vectorstore_faiss import VectorStore
from app.core.embeddings import get_embedding
import os, json, numpy as np

router = APIRouter(prefix="/api/mapping", tags=["mapping"])

# ✅ 경로 + 차원 통일
store = VectorStore(dimension=1536, index_path="app/storage/vectors.index")

# ===== 모델 정의 =====
class Hit(BaseModel):
    text: str
    score: Optional[float] = None
    meta: Optional[dict] = None

class FieldMapping(BaseModel):
    field: str
    hit: Optional[Hit]

class MappingRequest(BaseModel):
    spec_id: str
    required_fields: List[str]

class MappingResponse(BaseModel):
    spec_id: str
    results: List[FieldMapping]

# ===== 단순 매핑 (Spec → Doc) =====
@router.post("/simple", response_model=MappingResponse)
def mapping_simple(req: MappingRequest):
    if store.index is None:
        raise HTTPException(status_code=400, detail="Vector store not loaded. Upload first.")

    results: List[FieldMapping] = []
    for field in req.required_fields:
        q_vec = get_embedding(field)
        docs = store.search(q_vec, top_k=1)
        if docs:
            results.append(FieldMapping(
                field=field,
                hit=Hit(text=docs[0]["text"], score=docs[0]["score"])
            ))
        else:
            results.append(FieldMapping(field=field, hit=None))

    return MappingResponse(spec_id=req.spec_id, results=results)


# ===== 스펙 기반 매핑 (Spec → Doc) =====
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC_DIR = os.path.join(PROJECT_ROOT, "app", "specs")

@router.post("/from_spec/{spec_id}", response_model=MappingResponse)
def mapping_from_spec(spec_id: str):
    spec_path = os.path.join(SPEC_DIR, f"{spec_id}.json")
    if not os.path.exists(spec_path):
        raise HTTPException(status_code=404, detail=f"Spec {spec_id} not found")

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    required_fields = []
    for section in spec.get("sections", []):
        required_fields.extend(section.get("required_fields", []))

    return mapping_simple(MappingRequest(spec_id=spec_id, required_fields=required_fields))


# ===== 문서 기반 매핑 (Doc → Spec) =====
@router.post("/doc_to_spec/{spec_id}")
def mapping_doc_to_spec(spec_id: str, top_k: int = 1):
    spec_path = os.path.join(SPEC_DIR, f"{spec_id}.json")
    if not os.path.exists(spec_path):
        raise HTTPException(status_code=404, detail=f"Spec {spec_id} not found")

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    required_fields = []
    for section in spec.get("sections", []):
        required_fields.extend(section.get("required_fields", []))

    # 스펙 필드 임베딩
    field_vectors = [(field, get_embedding(field)) for field in required_fields]

    results = []
    for doc in store.docs:
        doc_vec = get_embedding(doc)
        scores = []
        for field, f_vec in field_vectors:
            dist = np.linalg.norm(np.array(doc_vec) - np.array(f_vec))
            scores.append((field, dist))
        # 가까운 스펙 필드 top_k 선택
        scores.sort(key=lambda x: x[1])
        top_matches = [field for field, _ in scores[:top_k]]

        results.append({
            "doc": doc,
            "matched_spec_fields": top_matches
        })

    return {"spec_id": spec_id, "results": results}
