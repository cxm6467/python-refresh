from pydantic import EmailStr
from sqlmodel import SQLModel, Field

from app.api.schemas.item import Category

class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=64)
    category: Category
    price_usd: float = Field(ge=0)
    in_stock: bool

class StoreManager(SQLModel, table=True):
    __tablename__ = "store_managers"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=64)
    email: EmailStr
    password_hash: str