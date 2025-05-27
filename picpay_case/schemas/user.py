from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date


class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    birthdate: date

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    email: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[date] = None
