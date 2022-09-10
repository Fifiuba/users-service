from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    password: str
    phone_number: str
    age: int


class UserResponse(UserBase):
    id: int
    name: str
    password: str
    phone_number: str
    age: int

    class Config:
        orm_mode = True

