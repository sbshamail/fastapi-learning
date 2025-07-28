from typing import Any, Optional
from fastapi.responses import JSONResponse

def api_response(
    code: int,
    detail: str,
    data: Optional[Any] = None,
    total: Optional[int] = None
):
    # ✅ Only process data if it’s not None
    if data is not None:
        # If it's a single SQLModel instance, convert it to a dict
        if hasattr(data, "model_dump"):
            data = data.model_dump()
        # If it's a list of SQLModel instances, convert each to dict
        elif isinstance(data, list) and data and hasattr(data[0], "model_dump"):
            data = [item.model_dump() for item in data]
        # If it's some other type (already serializable), leave it as is
        else:
            data = data

    # ✅ Build a JSONResponse with unified structure
    content={
            "success": 0 if code >= 300 else 1,  # 1 for success, 0 for error
            "detail": detail,                   # Description of the result
            "data": data,                       # Actual payload
        }
    
    if total is not None:
        content["total"] = total

    return JSONResponse(status_code=code, content=content)
