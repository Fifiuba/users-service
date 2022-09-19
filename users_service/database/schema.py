from pydantic import BaseModel


class UserBase(BaseModel):
    user_type: str
    name: str
    password: str
    phone_number: str
    age: int


class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    phone_number: str
    age: int

    class Config:
        orm_mode = True


class PassengerBase(BaseModel):
    id: int
    default_address: str


class DriverBase(BaseModel):
    id: int
    license_plate: str
    car_model: str


class UserLogInBase(BaseModel):
    name: str
    password: str
