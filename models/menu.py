# models/menu.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["bar_billing"]
menu_collection = db["menu_items"]
raw_material_collection = db["raw_materials"]
recipe_collection = db["recipes"]


def add_menu_item(name, category, item_type, unit, mrp, stock_qty=0):
    menu_collection.insert_one({
        "item_name": name,
        "category": category,
        "type": item_type,
        "unit": unit,
        "mrp": float(mrp),
        "stock_qty": int(stock_qty)
    })


def get_all_menu_items():
    return list(menu_collection.find())


def update_stock(item_name, quantity):
    item = menu_collection.find_one({"item_name": item_name})
    if item:
        category = item.get("category", "").lower()
        if category in ["liquor", "beer", "beverages"]:
            menu_collection.update_one(
                {"item_name": item_name},
                {"$inc": {"stock_qty": -quantity}}
            )
        elif category == "food":
            food_name = item.get("item_name")
            recipe = get_recipe_for_food(food_name)
            if recipe:
                for ingredient, qty_used in recipe.items():
                    raw_material_collection.update_one(
                        {"name": ingredient},
                        {"$inc": {"stock_qty": -qty_used * quantity}}
                    )


def get_stock(item_name):
    item = menu_collection.find_one({"item_name": item_name})
    category = item.get("category", "").lower() if item else ""
    if category in ["liquor", "beer", "beverages"]:
        return item.get("stock_qty", 0)
    return 0


def get_recipe_for_food(food_name):
    recipe_doc = recipe_collection.find_one({"food_name": food_name})
    return recipe_doc.get("ingredients", {}) if recipe_doc else {}


def add_raw_material(name, unit, stock_qty):
    raw_material_collection.update_one(
        {"name": name},
        {"$set": {"unit": unit}, "$inc": {"stock_qty": stock_qty}},
        upsert=True
    )


def get_all_raw_materials():
    return list(raw_material_collection.find())


def set_recipe_for_food(food_name, ingredients):
    # ingredients = {"rice": 100, "oil": 20}
    recipe_collection.update_one(
        {"food_name": food_name},
        {"$set": {"ingredients": ingredients}},
        upsert=True
    )
