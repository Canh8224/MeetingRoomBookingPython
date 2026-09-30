from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    user_name: str
    full_name: Optional[str] = None
    department: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    position_id: Optional[str] = None
    group_id: Optional[str] = None
    enabled: bool = True


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    user_id: int

    class Config:
        from_attributes = True