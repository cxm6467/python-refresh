import sqlite3

from models import Category, Item, ItemCreate, ItemUpdate

class Database:
    def __init__(self) -> None:
        # check_same_thread=False allows the connection to be used across threads
        # This is needed for FastAPI which runs endpoints in thread pools
        self.conn = sqlite3.connect("sqlite.db", check_same_thread=False)
        self.curr = self.conn.cursor()
        self.create_table("items")

    def create_table(self, name: str):
        # Create Table
        self.curr.execute(
            f"""CREATE TABLE IF NOT EXISTS {name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price_usd REAL NOT NULL,
                in_stock INTEGER NOT NULL
            )"""
        )
        self.conn.commit()

    def create_item(self, item: ItemCreate) -> Item:
        """Create a new item. Returns the created Item with auto-generated ID."""
        self.curr.execute(
            """
            INSERT INTO items (name, category, price_usd, in_stock)
            VALUES (?, ?, ?, ?)
            """,
            (item.name, item.category.value, item.price_usd, int(item.in_stock))
        )
        self.conn.commit()

        # Get the auto-generated ID
        item_id = self.curr.lastrowid
        if item_id is None:
            raise RuntimeError("Failed to get auto-generated ID from database")

        # Return the full Item with the ID
        return Item(
            id=item_id,
            name=item.name,
            category=item.category,
            price_usd=item.price_usd,
            in_stock=item.in_stock
        )

    def upsert_item(self, item: ItemCreate) -> Item:
        """Insert or update an item (upsert operation). For compatibility."""
        return self.create_item(item)

    def update_item(self, item_id: int, update: ItemUpdate) -> Item:
        """Update an existing item by ID. Returns the updated Item."""
        # First get the existing item
        existing = self.get_item(item_id)
        if existing is None:
            raise ValueError(f"Item with id {item_id} not found")

        # Apply updates
        update_data = update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(existing, field, value)

        # Save to database
        self.curr.execute(
            """
            UPDATE items
            SET name = ?,
                category = ?,
                price_usd = ?,
                in_stock = ?
            WHERE id = ?
            """,
            (existing.name, existing.category.value, existing.price_usd, int(existing.in_stock), item_id)
        )
        self.conn.commit()

        return existing

    def delete_item(self, item_id: int) -> None:
        """Delete an item by ID."""
        self.curr.execute(
            """
            DELETE FROM items WHERE id = ?
            """,
            (item_id,)
        )
        self.conn.commit()

    def get_item(self, item_id: int) -> Item | None:
        """Get a single item by ID. Returns None if not found."""
        self.curr.execute(
            """
            SELECT id, name, category, price_usd, in_stock
            FROM items
            WHERE id = ?
            """,
            (item_id,)
        )
        row = self.curr.fetchone()

        if row is None:
            return None

        return Item(
            id=row[0],
            name=row[1],
            category=Category(row[2]),
            price_usd=row[3],
            in_stock=bool(row[4])
        )

    def get_items(self) -> dict[int, Item]:
        """Get all items from the database as a dict keyed by ID."""
        self.curr.execute(
            """
            SELECT id, name, category, price_usd, in_stock
            FROM items
            """
        )
        rows = self.curr.fetchall()

        return {
            row[0]: Item(
                id=row[0],
                name=row[1],
                category=Category(row[2]),
                price_usd=row[3],
                in_stock=bool(row[4])
            )
            for row in rows
        }

    def close(self):
        """Close the database cursor and connection."""
        self.curr.close()
        self.conn.close()

