# core/embeddings.py
from openai import OpenAI
import numpy as np

client = OpenAI()

def get_embedding(text: str) -> np.ndarray:
    response = client.embeddings.create(
        model="text-embedding-3-small",  # 필요 시 large로 변경
        input=text
    )
    return np.array(response.data[0].embedding, dtype="float32")