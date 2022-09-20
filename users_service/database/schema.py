from typing import Union, List, Dict
from pydantic import BaseModel


class UserBase(BaseModel):
    user_type: str
    name: str
    password: str
    phone_number: Union[str, None] = None
    email: str
    age: Union[int, None] = None

class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    phone_number: Union[str, None] = None
    email: str
    age: Union[int, None] = None

    class Config:
        orm_mode = True

class UserRegisteredResponse(UserResponse):
    user_type: str


class PassengerBase(BaseModel):
    default_address: str


class DriverBase(BaseModel):
    license_plate: str
    car_model: str


class UserLogInBase(BaseModel):
    email: str
    password: str

class GoogleLogin(BaseModel):
    user_type: str
    name: str
    email: str
    googleId: int

class UserPatch(BaseModel):
    user_type: str
    fields: List[Dict]