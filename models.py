from enum import Enum
from pydantic import BaseModel, Field

class Category(str, Enum):
    GROCERY = "Grocery"
    HOUSEHOLD = "Household"
    ELECTRONICS = "Electronics"
    STATIONERY = "Stationery"
    PERSONAL_CARE = "Personal Care"
    APPAREL = "Apparel"
    HOME_IMPROVEMENT = "Home Improvement"
    PET = "Pet"


class Item(BaseModel):
    id: int
    name: str = Field(max_length=64)
    category: Category
    price_usd: float = Field(ge=0)
    in_stock: bool


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
