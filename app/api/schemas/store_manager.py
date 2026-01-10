from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class StoreManagerCreate(BaseModel):
    name: str = Field(max_length=64)
    email: EmailStr
    password_hash: str


class StoreManagerUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=64)
    email: EmailStr | None = None
    password: str | None = Field(default=None, description="New password - will be hashed")
    store_id: UUID | None = Field(default=None, description="Assign manager to a store")