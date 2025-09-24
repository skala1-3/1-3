from fastapi import APIRouter, UploadFile, HTTPException
from app.core.parsing import parse_document
from app.core.chunking import chunk_text
from app.core.embeddings import get_embedding
from app.core.vectorstore_faiss import VectorStore
import os

router = APIRouter()
store = VectorStore(dimension=1536, index_path="vectors.index")  # ✅ OpenAI 임베딩 기준 (1536차원)

@router.post("/api/documents/upload")
async def upload_document(file: UploadFile):
    try:
        # 1. uploads 디렉토리 생성
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        # 2. 파일 저장
        file_path = os.path.join(upload_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # 3. 문서 파싱 (경로 기반)
        text = parse_document(file_path)

        # 4. 텍스트 청킹
        chunks = chunk_text(text)

        # 5. 임베딩 생성
        vectors = [get_embedding(chunk) for chunk in chunks]

        # 6. 벡터스토어에 저장
        store.add_embeddings(vectors, chunks)
        store.save()

        return {
            "status": "ok",
            "filename": file.filename,
            "chunks": len(chunks)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
