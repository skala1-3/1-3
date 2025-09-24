# app/main.py
from fastapi import FastAPI
from app.api import documents_api

app = FastAPI()

# 라우터 등록
app.include_router(documents_api.router)

@app.get("/")
async def root():
    return {"message": "안녕하세요, ESG DB 연결 성공!"}
