from fastapi import FastAPI
from app.api import documents, search, mapping

app = FastAPI()

app.include_router(documents.router)
app.include_router(search.router)
app.include_router(mapping.router)




# uvicorn app.main:app --reload --port 8000

# ./.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000