from fastapi import APIRouter
from fastapi_utils.cbv import cbv

user_router = APIRouter()


@cbv(user_router)
class UserController:
    @user_router.get("/users/", tags=["users"])
    def read_users():
        return [{"username": "Rick"}, {"username": "Morty"}]
