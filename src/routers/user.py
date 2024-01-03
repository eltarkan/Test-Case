import os
import bcrypt
import jwt
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from src.database.repository.user import get_user_with_email, create_user
from src.middlewares import jwt_middleware
from src.requests import LoginRequest

user_router = APIRouter()


@user_router.post("/login")
def login(login_request: LoginRequest):
    user = get_user_with_email(login_request.email)
    if not user:
        return {"status": "ERROR", "message": "User not found"}

    if bcrypt.checkpw(login_request.password.encode('utf8'), user.password.encode('utf8')) is False:
        return {"status": "ERROR", "message": "Wrong password"}
    token = jwt.encode({
        "email": user.email
    }, os.getenv("JWT_SECRET_KEY", "guardian"), algorithm="HS256")
    # return json response with header
    return JSONResponse({"status": "OK", "token": token})


@user_router.get("/validate", dependencies=[Depends(jwt_middleware)])
def validate_token(request: Request):
    token = jwt.encode({
        "email": request.state.user.email
    }, os.getenv("JWT_SECRET_KEY", "guardian"), algorithm="HS256")

    return {"status": "OK", "token": token}


@user_router.post("/register")
def register(login_request: LoginRequest):
    try:
        user = create_user(login_request.email, login_request.password)
        return {"status": "OK", "user": user}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
