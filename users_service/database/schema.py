from typing import Optional, Union, List, Dict
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    user_type: str
    name: str
    phone_number: Union[str, None] = None
    email: str
    password: str
    picture: Union[str, None] = None
    age: Union[int, None] = None


class UserResponse(BaseModel):
    id: int
    name: str
    phone_number: Union[str, None] = None
    email: str
    age: Union[int, None] = None
    picture: Union[str, None] = None
    isBlock: bool

    class Config:
        orm_mode = True


class UserInfoResponse(BaseModel):
    name: str
    phone_number: Union[str, None] = None
    email: str
    age: Union[int, None] = None

    class Config:
        orm_mode = True


class UserRegisteredResponse(UserResponse):
    id: int
    user_type: str
    name: str
    phone_number: Union[str, None] = None
    email: str
    age: Union[int, None] = None

    class Config:
        orm_mode = True


class PassengerBase(BaseModel):
    default_address: str


class DriverBase(BaseModel):
    license_plate: str
    car_model: str


class UserLogInBase(BaseModel):
    user_type: str
    token: str


class GoogleLogin(BaseModel):
    user_type: str
    token: str


class UserEditFields(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None
    age: Optional[str] = None


class PassengerEditFields(BaseModel):
    default_address: Optional[str] = None


class DriverEditFields(BaseModel):
    license_plate: Optional[str] = None
    car_model: Optional[str] = None


class UserPatch(BaseModel):
    user_type: str
    fields: List[Dict]


class TypeOfUser(BaseModel):
    user_type: Optional[str] = None


class UserScore(BaseModel):
    user_type: str
    score: int = Field(..., ge=1, le=5)
    opinion: Optional[str] = None


class BlockUser(BaseModel):
    block: bool
