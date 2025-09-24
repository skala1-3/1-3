# core/chunking.py
from typing import List

def chunk_text(text: str) -> List[str]:
    """
    줄바꿈(\n)을 기준으로 텍스트를 나눠 각 줄을 하나의 청크로 반환.
    공백이거나 빈 줄은 제거됨.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines