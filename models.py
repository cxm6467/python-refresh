from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    category: str
    price_usd: float
    in_stock: bool


class ItemCreate(BaseModel):
    name: str
    category: str
    price_usd: float
    in_stock: bool


class ItemUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    price_usd: float | None = None
    in_stock: bool | None = None
