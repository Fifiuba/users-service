from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    password: str
    phone_number: str
    age: int


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
