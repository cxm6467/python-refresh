from pydantic import BaseModel
from sqlmodel import Field
from app.database.models import Category


class ItemCreate(BaseModel):
    name: str = Field(max_length=64)
    category: Category
    price_usd: float = Field(ge=0)
    in_stock: bool


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=64)
    category: Category | None = None
    price_usd: float | None = Field(default=None, ge=0)
    in_stock: bool | None = None

