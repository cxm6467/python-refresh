from fastapi import FastAPI, HTTPException
from scalar_fastapi import get_scalar_api_reference

from database import db
from helpers import find_item_by_id
from models import Item, ItemCreate, ItemUpdate

app = FastAPI()


# GET /items/{item_id}
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items", response_model=dict[int, Item])
def get_items() -> dict[int, Item]:
    return db["items"]


# POST /items
@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate) -> Item:
    next_id = max(db["items"].keys(), default=0) + 1
    created = Item(id=next_id, **item.model_dump())
    db["items"][next_id] = created
    return created


# PATCH /items/{item_id}
@app.patch("/items/{item_id}", response_model=Item)
def update_item(item_id: int, update: ItemUpdate) -> Item:
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    return item


# DELETE /items/{item_id}
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    item = find_item_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    del db["items"][item_id]


# Scalar docs
@app.get("/scalar", include_in_schema=False)
def get_scalar_api_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
