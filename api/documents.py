from fastapi import APIRouter, UploadFile
from core.parsing import parse_document
from core.chunking import chunk_text
from core.embeddings import get_embedding
from core.vectorstore_faiss import VectorStore  # ✅ 이름 통일
import os

router = APIRouter()
store = VectorStore(dimension=1536, index_path="vectors.index")  # ✅ 이름 맞게 수정

@router.post("/api/documents/upload")
async def upload_document(file: UploadFile):
    # 1. uploads 디렉토리 자동 생성
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # 2. 파일 저장
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 3. 문서 파싱
    text = parse_document(file_path)

    # 4. 텍스트 청킹
    chunks = chunk_text(text)

    # 5. 임베딩 생성 및 저장
    vectors = [get_embedding(chunk) for chunk in chunks]
    store.add_embeddings(vectors)
    store.save()

    return {
        "status": "ok",
        "filename": file.filename,
        "chunks": len(chunks)
    }
