from fastapi import Request, HTTPException
import os
import jwt
from src.database.repository.user import get_user_with_email


async def jwt_middleware(request: Request):
    _token = request.headers.get("Authorization")
    if not _token:
        raise HTTPException(status_code=401, detail="Token not found")

    token = _token.split(" ")[1]
    try:
        decoded = jwt.decode(token, os.getenv("JWT_SECRET_KEY", "guardian"), algorithms=["HS256"])
        _user = get_user_with_email(decoded.get("email"))
        if not _user:
            raise HTTPException(status_code=401, detail="Invalid JWT token")

        request.state.token = decoded
        request.state.user = _user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
