from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

def api_response(
    code: int,
    detail: str,
    data: Optional[Any] = None,
    total: Optional[int] = None
):
    content = {
        "success": 1 if code < 300 else 0,
        "detail": detail,
        "data": jsonable_encoder(data),
    }

    if total is not None:
        content["total"] = total

    # Raise error if code >= 400
    if code >= 400:
        raise HTTPException(status_code=code, detail=detail)

    return JSONResponse(status_code=code, content=content)
