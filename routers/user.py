from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()


@user_router.post("/login", tags=['auth'])
def login(user: User) -> User:
    """_summary_

    Args:
        user (User): _description_

    Returns:
        User: user obcjt
    """
    if user.email=="admin@gmail.com" and user.password == "admin":
        token =  create_token(data= user.dict())
        return JSONResponse(content=token)