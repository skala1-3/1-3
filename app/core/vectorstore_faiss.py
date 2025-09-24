import faiss, os, pickle
import numpy as np

class VectorStore:
    def __init__(self, dimension: int = 384, index_path: str = "storage/vectors.index"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = None
        self.docs = []

        if os.path.exists(index_path):
            self.load()

    def add_embeddings(self, embeddings, docs):
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
        arr = np.array(embeddings).astype("float32")

        # ✅ 벡터 차원 강제 정규화
        if arr.ndim == 1:      # (dim,) → (1, dim)
            arr = arr.reshape(1, -1)
        elif arr.ndim == 2 and arr.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension mismatch: expected {self.dimension}, got {arr.shape[1]}")

        self.index.add(arr)
        self.docs.extend(docs)

    def search(self, query_vec, top_k: int = 5):
        if self.index is None:
            return []
        q = np.array(query_vec).astype("float32")
        if q.ndim == 1:
            q = q.reshape(1, -1)
        D, I = self.index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx < len(self.docs):
                results.append({"text": self.docs[idx], "score": float(dist)})
        return results

    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path + ".meta", "wb") as f:
            pickle.dump(self.docs, f)

    def load(self):
        self.index = faiss.read_index(self.index_path)
        with open(self.index_path + ".meta", "rb") as f:
            self.docs = pickle.load(f)
