# chunk_service.py
def chunk_text(text: str, max_tokens: int = 500, overlap: int = 50) -> list[str]:
    """
    텍스트를 일정 토큰 단위로 청킹하는 함수
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens - overlap):
        chunk = " ".join(words[i:i+max_tokens])
        chunks.append(chunk)
    return chunks
