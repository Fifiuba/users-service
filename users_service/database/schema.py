from pydantic import BaseModel


class UserBase(BaseModel):
    user_type: str
    name: str
    password: str
    phone_number: str
    email: str
    age: int


class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    phone_number: str
    email: str
    age: int

    class Config:
        orm_mode = True


class PassengerBase(BaseModel):
    default_address: str


class DriverBase(BaseModel):
    license_plate: str
    car_model: str


class UserLogInBase(BaseModel):
    email: str
    password: str

class GoogleLogin(BaseModel):
    email: str
    password: str