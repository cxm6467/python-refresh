import json
import sqlite3

from models import Category, Item

# Load seed data from JSON
with open("database.json") as f:
    data = json.load(f)

connection = sqlite3.connect("sqlite.db")
cursor = connection.cursor()

# Create Table
cursor.execute(
    """CREATE TABLE IF NOT EXISTS items(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price_usd REAL NOT NULL,
        in_stock INTEGER NOT NULL
    )"""
)

# Prepare items for insertion
items_to_insert = [
    (
        item["id"],
        item["name"],
        item["category"],
        item["price_usd"],
        int(item["in_stock"]),
    )
    for item in data["items"].values()
]

# Insert items into database
cursor.executemany(
    """INSERT OR IGNORE INTO items (id, name, category, price_usd, in_stock)
    VALUES (?, ?, ?, ?, ?)""",
    items_to_insert,
)

connection.commit()
connection.close()

db: dict[str, dict[int, Item]] = {
    "items": {
        1: Item(
            id=1,
            name="Whole Bean Coffee (12 oz)",
            category=Category.GROCERY,
            price_usd=12.99,
            in_stock=True,
        ),
        2: Item(
            id=2,
            name="Dish Soap (24 oz)",
            category=Category.HOUSEHOLD,
            price_usd=4.49,
            in_stock=True,
        ),
        3: Item(
            id=3,
            name="USB-C Charging Cable (1m)",
            category=Category.ELECTRONICS,
            price_usd=9.99,
            in_stock=True,
        ),
        4: Item(
            id=4,
            name="Notebook (College Ruled)",
            category=Category.STATIONERY,
            price_usd=2.29,
            in_stock=True,
        ),
        5: Item(
            id=5,
            name="Shampoo (16 oz)",
            category=Category.PERSONAL_CARE,
            price_usd=7.79,
            in_stock=False,
        ),
        6: Item(
            id=6,
            name="Extra Virgin Olive Oil (500ml)",
            category=Category.GROCERY,
            price_usd=11.49,
            in_stock=True,
        ),
        7: Item(
            id=7,
            name="Men's Cotton T-Shirt (M)",
            category=Category.APPAREL,
            price_usd=14.99,
            in_stock=True,
        ),
        8: Item(
            id=8,
            name="LED Light Bulb (60W Equivalent)",
            category=Category.HOME_IMPROVEMENT,
            price_usd=3.99,
            in_stock=True,
        ),
        9: Item(
            id=9,
            name="Toothpaste (6 oz)",
            category=Category.PERSONAL_CARE,
            price_usd=3.49,
            in_stock=False,
        ),
        10: Item(
            id=10,
            name="Dog Treats (8 oz)",
            category=Category.PET,
            price_usd=6.99,
            in_stock=True,
        ),
    }
}
