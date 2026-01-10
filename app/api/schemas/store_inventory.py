from pydantic import BaseModel
from sqlmodel import Field
from app.database.models import Region


class StoreInventoryCreate(BaseModel):
    name: str = Field(max_length=64)
    region: Region


class StoreInventoryUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=64)
    region: Region | None = None
