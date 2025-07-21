# models/orders.py

orders = {}

def save_order_for_table(table_no, kot_data):
    orders[table_no] = kot_data

def get_order_for_table(table_no):
    return orders.get(table_no)
