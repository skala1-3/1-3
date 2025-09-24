from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Union
import re
import pint

# FastAPI 인스턴스
app = FastAPI()

# Pint 단위 등록
ureg = pint.UnitRegistry()
# ESG 관련 사용자 정의 단위 추가
ureg.define("kgCO2e = kilogram")
ureg.define("tCO2e = 1000 * kgCO2e")
ureg.define("gCO2e = 0.001 * kgCO2e")

# -------- Root ----------
@app.get("/")
async def root():
    return {"message": "안녕하세요, ESG 초안 API가 실행 중입니다."}

# -------- 요청 스키마 ----------
class UnitConvertRequest(BaseModel):
    value: float
    from_unit: str
    to_unit: str

class CleanDataRequest(BaseModel):
    raw_value: Union[str, float, None]
    decimals: Optional[int] = 2

# -------- 단위 변환 API ----------
@app.post("/api/tools/convert-units")
async def convert_units(req: UnitConvertRequest):
    try:
        q = req.value * ureg(req.from_unit)
        result = q.to(req.to_unit).magnitude
        return {
            "input": req.value,
            "from": req.from_unit,
            "to": req.to_unit,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}

# -------- 데이터 클리닝 API ----------
@app.post("/api/tools/clean-data")
async def clean_data(req: CleanDataRequest):
    val = req.raw_value
    if val is None or str(val).strip() in ["", "-", "N/A", "n/a", "na"]:
        return {"cleaned": None}
    try:
        num = float(re.sub(r"[^\d\.\-]", "", str(val)))
        num = round(num, req.decimals)
        return {"cleaned": num}
    except Exception:
        cleaned_str = re.sub(r"\s+", " ", str(val)).strip()
        return {"cleaned": cleaned_str}
