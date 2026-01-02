from database import Database
from models import Item


def find_item_by_id(db: Database, item_id: int) -> Item | None:
    """Find an item by ID using the Database instance."""
    return db.get_item(item_id)
