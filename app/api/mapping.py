from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from app.core.vectorstore_faiss import VectorStore
from app.core.embeddings import get_embedding
import os

router = APIRouter(prefix="/api/mapping", tags=["mapping"])

# ✅ 벡터스토어 로드 (이미 documents.py에서 저장된 index 재활용)
store = VectorStore(dimension=384, index_path="storage/vectors.index")

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


# ===== 단순 매핑 (필드별 가장 가까운 청크 1개) =====
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


# ===== 스펙 기반 매핑 (/api/mapping/from_spec/{spec_id}) =====
import json

@router.post("/from_spec/{spec_id}", response_model=MappingResponse)
def mapping_from_spec(spec_id: str):
    spec_path = os.path.join("specs", f"{spec_id}.json")
    if not os.path.exists(spec_path):
        raise HTTPException(status_code=404, detail=f"Spec {spec_id} not found")

    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    required_fields = []
    for section in spec.get("sections", []):
        required_fields.extend(section.get("required_fields", []))

    return mapping_simple(MappingRequest(spec_id=spec_id, required_fields=required_fields))
