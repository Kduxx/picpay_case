from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    name: str


class UserUpdate(UserBase):
    name: Optional[str] = None


class UserResponse(UserBase):
    """"""
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )
