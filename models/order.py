from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from db.mongo import db

orders_collection = db["orders"]  # already connected through db.mongo

def merge_items(existing_items, new_items):
    """
    Merge new items into existing order. If the same item exists, increase quantity.
    """
    item_map = {item['name']: item for item in existing_items}

    for new_item in new_items:
        name = new_item['name']
        if name in item_map:
            item_map[name]['qty'] += new_item['qty']
        else:
            item_map[name] = new_item

    return list(item_map.values())

def create_order(table_no, items):
    """
    Create or update an ongoing order for a table.
    """
    existing = orders_collection.find_one({"table_no": table_no, "status": "ongoing"})

    if existing:
        updated_items = merge_items(existing['items'], items)
        orders_collection.update_one(
            {"_id": existing['_id']},
            {
                "$set": {
                    "items": updated_items,
                    "updated_at": datetime.now()
                }
            }
        )
        return str(existing['_id'])
    else:
        order = {
            "table_no": table_no,
            "items": items,
            "status": "ongoing",  # or "active" depending on your business logic
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        result = orders_collection.insert_one(order)
        return str(result.inserted_id)

def get_order_by_table(table_no):
    """
    Get the current ongoing order for a table.
    """
    return orders_collection.find_one({"table_no": table_no, "status": "ongoing"})

def get_all_active_orders():
    """
    Get all orders marked as active (for kitchen panel).
    """
    return list(orders_collection.find({"status": "active"}))

def finalize_order(table_no):
    """
    Finalize an ongoing order (mark it completed).
    """
    result = orders_collection.update_one(
        {"table_no": table_no, "status": "ongoing"},
        {
            "$set": {
                "status": "completed",
                "updated_at": datetime.now()
            }
        }
    )
    return result.modified_count > 0
