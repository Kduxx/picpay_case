from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from datetime import datetime, date


class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    birthdate: date

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )

    @field_validator("birthdate", mode="before")
    def validate_birthdate(cls, v):  # pylint: disable=no-self-argument
        bd = datetime.strptime(v, "%Y-%m-%d").date() \
            if isinstance(v, str) else v
        if bd > date.today():
            raise ValueError("Birth date cannot be in the future.")
        elif bd == date.today():
            raise ValueError("Birth date cannot be today.")
        return v


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
