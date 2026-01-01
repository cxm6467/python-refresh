from database import db
from models import Item


def find_item_by_id(item_id: int) -> Item | None:
    return db["items"].get(item_id)
