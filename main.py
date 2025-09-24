# main.py (1-3 폴더 바로 아래)
from fastapi import FastAPI
from api.documents import router as documents_router

app = FastAPI(title="Vectorizer API")
app.include_router(documents_router)

@app.get("/")
def health():
    return {"ok": True}