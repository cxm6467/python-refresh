from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str = Field(max_length=64)
    category: str = Field(max_length=128)
    price_usd: float = Field(ge=0)
    in_stock: bool


class ItemCreate(BaseModel):
    name: str = Field(max_length=64)
    category: str = Field(max_length=128)
    price_usd: float = Field(ge=0)
    in_stock: bool


class ItemUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=64)
    category: str | None = Field(default=None, max_length=128)
    price_usd: float | None = Field(default=None, ge=0)
    in_stock: bool | None = None
