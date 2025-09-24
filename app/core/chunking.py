# core/chunking.py
from typing import List

def chunk_text(text: str) -> List[str]:
    """
    첫 줄(제목)은 제외하고, 줄바꿈(\n)을 기준으로 텍스트를 나눔.
    공백이거나 빈 줄은 제거됨.
    """
    # 1. 줄 단위 분리
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # 2. 제목(첫 줄) 제거
    if not lines:
        return []
    content_lines = lines[1:]  # ✅ 첫 줄 제외

    # 3. 남은 줄을 청크로 반환
    return content_lines
