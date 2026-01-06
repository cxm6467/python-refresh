from pydantic import BaseModel, EmailStr, Field


class StoreManagerCreate(BaseModel):
    name: str = Field(max_length=64)
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)

class StoreManagerUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=64)
    email: EmailStr | None = None
    password_hash: str | None = Field(default=None, min_length=8, max_length=32)