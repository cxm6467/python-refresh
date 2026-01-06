from pydantic import BaseModel, EmailStr, Field


class StoreManagerCreate(BaseModel):
    name: str = Field(max_length=64)
    email: EmailStr
    password_hash: str

# class StoreManagerUpdate(BaseModel):
#    name: str | None = Field(default=None, max_length=64)
#    email: EmailStr | None = None
#    password_hash: str | None = None