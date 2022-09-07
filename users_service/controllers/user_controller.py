from fastapi import APIRouter, Depends, HTTPException

user_router = APIRouter()

@user_router.get("/users/", tags=["users"])
def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]