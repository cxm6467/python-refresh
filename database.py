from models import Item

db: dict[str, dict[int, Item]] = {
    "items": {
        1: Item(
            id=1,
            name="Whole Bean Coffee (12 oz)",
            category="grocery",
            price_usd=12.99,
            in_stock=True,
        ),
        2: Item(
            id=2,
            name="Dish Soap (24 oz)",
            category="household",
            price_usd=4.49,
            in_stock=True,
        ),
        3: Item(
            id=3,
            name="USB-C Charging Cable (1m)",
            category="electronics",
            price_usd=9.99,
            in_stock=True,
        ),
        4: Item(
            id=4,
            name="Notebook (College Ruled)",
            category="stationery",
            price_usd=2.29,
            in_stock=True,
        ),
        5: Item(
            id=5,
            name="Shampoo (16 oz)",
            category="personal_care",
            price_usd=7.79,
            in_stock=False,
        ),
        6: Item(
            id=6,
            name="Extra Virgin Olive Oil (500ml)",
            category="grocery",
            price_usd=11.49,
            in_stock=True,
        ),
        7: Item(
            id=7,
            name="Men's Cotton T-Shirt (M)",
            category="apparel",
            price_usd=14.99,
            in_stock=True,
        ),
        8: Item(
            id=8,
            name="LED Light Bulb (60W Equivalent)",
            category="home_improvement",
            price_usd=3.99,
            in_stock=True,
        ),
        9: Item(
            id=9,
            name="Toothpaste (6 oz)",
            category="personal_care",
            price_usd=3.49,
            in_stock=False,
        ),
        10: Item(
            id=10,
            name="Dog Treats (8 oz)",
            category="pet",
            price_usd=6.99,
            in_stock=True,
        ),
    }
}
