from fastapi import FastAPI, HTTPException
from scalar_fastapi import get_scalar_api_reference

from database import Database
from models import Item, ItemCreate, ItemUpdate

app = FastAPI()
db = Database()

# GET /items/{item_id}
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    item = db.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items", response_model=dict[int, Item])
def get_items() -> dict[int, Item]:
    return db.get_items()


# POST /items
@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate) -> Item:
    created = db.create_item(item)
    return created


# PATCH /items/{item_id}
@app.patch("/items/{item_id}", response_model=Item)
def update_item(item_id: int, update: ItemUpdate) -> Item:
    try:
        updated = db.update_item(item_id, update)
        return updated
    except ValueError:
        raise HTTPException(status_code=404, detail="Item not found")


# DELETE /items/{item_id}
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int) -> None:
    item = db.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete_item(item_id)


# Scalar docs
@app.get("/scalar", include_in_schema=False)
def get_scalar_api_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )

db.close()
