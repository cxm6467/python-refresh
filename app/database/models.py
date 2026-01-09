from enum import Enum
from pydantic import EmailStr
from sqlmodel import Column, Relationship, SQLModel, Field
from uuid import UUID, uuid4
from sqlalchemy.dialects import postgresql


class Category(str, Enum):
    GROCERY = "Grocery"
    HOUSEHOLD = "Household"
    ELECTRONICS = "Electronics"
    STATIONERY = "Stationery"
    PERSONAL_CARE = "Personal Care"
    APPAREL = "Apparel"
    HOME_IMPROVEMENT = "Home Improvement"
    PET = "Pet"

class Region(str, Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"
    CENTRAL = "Central"
    NORTH_EAST = "North East"
    NORTH_WEST = "North West"
    SOUTH_EAST = "South East"
    SOUTH_WEST = "South West"
    NORTH_CENTRAL = "North Central"
    SOUTH_CENTRAL = "South Central"


class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: UUID | None = Field(
            default_factory=uuid4,
            sa_column=Column[UUID](
                postgresql.UUID(as_uuid=True),
                primary_key=True,
                nullable=False
            )
        )
    name: str = Field(max_length=64)
    category: Category
    price_usd: float = Field(ge=0)
    in_stock: bool

    store_id: UUID = Field(foreign_key="stores.id")
    store: "Store" = Relationship(back_populates="items")

    store_inventory_id: UUID | None = Field(foreign_key="store_inventories.id", default=None)
    store_inventory: "StoreInventory | None" = Relationship(back_populates="items")


class Store(SQLModel, table=True):
    __tablename__ = "stores"

    id: UUID | None = Field(
        default_factory=uuid4,
        sa_column=Column[UUID](
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )
    name: str = Field(max_length=64)
    location: str = Field(max_length=128)

    items: list[Item] = Relationship(back_populates="store")
    store_manager: "StoreManager | None" = Relationship(back_populates="store")


class StoreManager(SQLModel, table=True):
    __tablename__ = "store_managers"

    id: UUID | None = Field(
        default_factory=uuid4,
        sa_column=Column[UUID](
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )
    name: str = Field(max_length=64)
    email: EmailStr = Field(unique=True, index=True)
    password_hash: str = Field(exclude=True)

    store_id: UUID | None = Field(foreign_key="stores.id", default=None, unique=True)
    store: "Store | None" = Relationship(back_populates="store_manager")


class StoreInventory(SQLModel, table=True):
    __tablename__ = "store_inventories"

    id: UUID | None = Field(
        default_factory=uuid4,
        sa_column=Column[UUID](
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )
    name: str = Field(max_length=64)
    region: Region

    items: list[Item] = Relationship(back_populates="store_inventory")