from pymongo import MongoClient

client = MongoClient()
db = client['bar_system']
tables = db['tables']

def get_all_tables():
    return list(tables.find())

def initialize_tables(total=20):
    if tables.count_documents({}) == 0:
        for i in range(1, total + 1):
            tables.insert_one({"table_no": i, "status": "available"})

def add_table(table_no):
    if not tables.find_one({"table_no": table_no}):
        tables.insert_one({"table_no": table_no, "status": "available"})

def remove_table(table_no):
    tables.delete_one({"table_no": table_no})

def set_table_status(table_no, status):
    tables.update_one({"table_no": table_no}, {"$set": {"status": status}})