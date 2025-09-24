# embedding_service.py
from openai import OpenAI
client = OpenAI()

def generate_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """
    OpenAI 임베딩 API 호출
    """
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding
