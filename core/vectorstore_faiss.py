# core/vectorstore_faiss.py

import os
import pickle
from typing import List, Dict, Any
import numpy as np

try:
    import faiss
    _HAVE_FAISS = True
except ImportError:
    _HAVE_FAISS = False


class VectorStore:
    def __init__(self, dimension: int, index_path: str = "vectors.index"):
        self.dimension = dimension
        self.index_path = index_path
        self._metas: List[Dict[str, Any]] = []
        self._embs: np.ndarray | None = None

        if _HAVE_FAISS:
            self.index = faiss.IndexFlatIP(dimension)
        else:
            self.index = None

        if os.path.exists(index_path):
            self.load()

    def _normalize(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=np.float32)
        return X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)

    def add(self, embeddings: np.ndarray, metadatas: List[Dict[str, Any]]):
        X = self._normalize(embeddings)
        if _HAVE_FAISS:
            self.index.add(X)
        else:
            if self._embs is None:
                self._embs = X
            else:
                self._embs = np.vstack([self._embs, X])
        self._metas.extend(metadatas)

    def add_embeddings(self, embeddings: List[np.ndarray]):
        """
        ✅ 기존 documents.py 코드 호환용
        단순 벡터 리스트를 받아서 메타데이터 없이 저장하는 인터페이스
        """
        embeddings_np = np.array(embeddings, dtype=np.float32)
        self.add(embeddings_np, metadatas=[{}] * len(embeddings))

    def save(self):
        if _HAVE_FAISS:
            faiss.write_index(self.index, self.index_path)
            with open(self.index_path + ".meta.pkl", "wb") as f:
                pickle.dump(self._metas, f)
        else:
            with open(self.index_path, "wb") as f:
                pickle.dump({"metas": self._metas, "embs": self._embs}, f)

    def load(self):
        if _HAVE_FAISS:
            self.index = faiss.read_index(self.index_path)
            meta_path = self.index_path + ".meta.pkl"
            if os.path.exists(meta_path):
                with open(meta_path, "rb") as f:
                    self._metas = pickle.load(f)
        else:
            with open(self.index_path, "rb") as f:
                data = pickle.load(f)
                self._metas = data["metas"]
                self._embs = data["embs"]

    def search(self, query: np.ndarray, k: int = 5) -> List[Dict[str, Any]]:
        q = self._normalize(query.reshape(1, -1))
        if _HAVE_FAISS:
            scores, indices = self.index.search(q, k)
            return [
                {"score": float(scores[0][i]), "metadata": self._metas[idx]}
                for i, idx in enumerate(indices[0]) if 0 <= idx < len(self._metas)
            ]
        else:
            sims = self._embs @ q.T if self._embs is not None else []
            idxs = np.argsort(-sims.ravel())[:k]
            return [
                {"score": float(sims[idx]), "metadata": self._metas[idx]}
                for idx in idxs if 0 <= idx < len(self._metas)
            ]

