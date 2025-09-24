from fastapi import APIRouter, HTTPException
from app.core.vectorstore_faiss import VectorStore
from app.core.embeddings import get_embedding
from app.core.bm25_utils import build_bm25
from sentence_transformers import CrossEncoder
import numpy as np

router = APIRouter(prefix="/api/search", tags=["search"])

# ✅ 경로 + 차원 통일
store = VectorStore(dimension=1536, index_path="app/storage/vectors.index")
bm25 = None
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

@router.on_event("startup")
def init_bm25():
    global bm25
    if store.docs:
        bm25 = build_bm25(store.docs)

@router.post("/faiss")
def faiss_search(query: str, top_k: int = 5):
    q_vec = get_embedding(query)
    print("쿼리 임베딩 길이:", len(q_vec))
    print("검색 시점 인덱스 개수:", store.index.ntotal)
    return store.search(q_vec, top_k=top_k)

@router.post("/bm25")
def bm25_search(query: str, top_k: int = 5):
    if bm25 is None:
        raise HTTPException(status_code=400, detail="BM25 not available")
    scores = bm25.get_scores(query.split())
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [{"text": store.docs[i], "score": float(scores[i])} for i in top_idx]

@router.post("/hybrid")
def hybrid_search(query: str, top_k: int = 5, alpha: float = 0.5):
    faiss_res = faiss_search(query, top_k=top_k*2)
    bm25_res = bm25_search(query, top_k=top_k*2)

    def norm(vals):
        arr = np.array(vals)
        return (arr - arr.min()) / (arr.max() - arr.min()) if arr.max() > arr.min() else np.zeros_like(arr)

    pool = {}
    for r in faiss_res:
        pool[r["text"]] = {"faiss": r["score"], "bm25": 0}
    for r in bm25_res:
        pool.setdefault(r["text"], {"faiss": 0, "bm25": 0})
        pool[r["text"]]["bm25"] = r["score"]

    nf, nb = norm([pool[t]["faiss"] for t in pool]), norm([pool[t]["bm25"] for t in pool])
    results = []
    for i, t in enumerate(pool):
        score = alpha * nf[i] + (1 - alpha) * nb[i]
        results.append({"text": t, "score": float(score)})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

@router.post("/rerank")
def rerank_search(query: str, candidates: list[str], top_k: int = 5):
    pairs = [(query, c) for c in candidates]
    scores = reranker.predict(pairs).tolist()
    results = [{"text": c, "score": float(s)} for c, s in zip(candidates, scores)]
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
