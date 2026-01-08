from typing import Any


from pydantic import EmailStr
from sqlmodel import Column, Relationship, SQLModel, Field
from uuid import UUID, uuid4
from app.api.schemas.item import Category
from sqlalchemy.dialects import postgresql

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

    store_manager_id: UUID = Field(foreign_key="store_managers.id")
    store_manager: "StoreManager" = Relationship(
        back_populates="items",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

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
    email: EmailStr
    password_hash: str

    items: list[Item] = Relationship(
        back_populates="store_manager",
        sa_relationship_kwargs={"lazy": "selectin"}
    )