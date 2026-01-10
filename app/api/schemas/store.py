from pydantic import BaseModel
from sqlmodel import Field


class StoreCreate(BaseModel):
    name: str = Field(max_length=64)
    location: str = Field(max_length=128)


class StoreUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=64)
    location: str | None = Field(default=None, max_length=128)
