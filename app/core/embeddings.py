import os
from openai import OpenAI


# ✅ 환경변수에서 OPENAI_API_KEY 읽기
API_KEY = ""
if not API_KEY:
    raise ValueError("환경변수 OPENAI_API_KEY가 설정되지 않았습니다.")

client = OpenAI(api_key=API_KEY)


def get_embedding(text: str):
    """
    OpenAI 임베딩 API를 사용해 1536차원 벡터를 생성합니다.
    모델: text-embedding-3-small
    """
    response = client.embeddings.create(
        model="text-embedding-3-small", input=text  # ✅ 1536차원
    )
    return response.data[0].embedding
