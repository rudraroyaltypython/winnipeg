# ui/settings_view.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from models.tables import add_table, remove_table, get_all_tables
from models.menu import add_menu_item, get_all_menu_items, update_stock

def open_menu_settings(root):
    win = tb.Toplevel(root)
    win.title("⚙️ Settings - Menu & Table Management")
    win.geometry("800x650")
    win.grab_set()

    notebook = tb.Notebook(win)
    notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # ---------------- Tab 1: Table Management ---------------- #
    table_tab = tb.Frame(notebook)
    notebook.add(table_tab, text="🪑 Manage Tables")

    tb.Label(table_tab, text="Add New Table", font=("Helvetica", 14, "bold")).pack(pady=10)
    table_no_entry = tb.Entry(table_tab, width=30)
    table_no_entry.pack()

    def refresh_table_dropdown():
        table_dropdown['values'] = [f"Table {t['table_no']}" for t in get_all_tables()]

    def add_table_action():
        tno = table_no_entry.get()
        if tno.isdigit():
            add_table(int(tno))
            messagebox.showinfo("Success", f"Table {tno} added.")
            table_no_entry.delete(0, 'end')
            refresh_table_dropdown()
        else:
            messagebox.showwarning("Invalid", "Please enter a valid table number.")

    tb.Button(table_tab, text="➕ Add Table", command=add_table_action, bootstyle="success").pack(pady=5)

    # Remove Table
    tb.Label(table_tab, text="Remove Table", font=("Helvetica", 14, "bold")).pack(pady=20)
    table_dropdown = tb.Combobox(table_tab, width=30)
    table_dropdown.pack()
    refresh_table_dropdown()

    def remove_table_action():
        selected = table_dropdown.get()
        if selected.startswith("Table"):
            tno = int(selected.split()[1])
            remove_table(tno)
            messagebox.showinfo("Removed", f"Table {tno} removed.")
            refresh_table_dropdown()
        else:
            messagebox.showwarning("Select Table", "Please select a table to remove.")

    tb.Button(table_tab, text="➖ Remove Table", command=remove_table_action, bootstyle="danger").pack(pady=5)

    # ---------------- Shared Function to Add Stock ---------------- #
    def stock_entry_widget(parent):
        stock_label = tb.Label(parent, text="Initial Stock Quantity", font=("Helvetica", 10))
        stock_label.pack(pady=5)
        stock_entry = tb.Entry(parent, width=40)
        stock_entry.insert(0, "Enter Quantity in Stock")
        stock_entry.pack(pady=5)
        return stock_entry

    # ---------------- Tab 2: Liquor Menu ---------------- #
    liquor_tab = tb.Frame(notebook)
    notebook.add(liquor_tab, text="🥃 Liquor Menu")

    tb.Label(liquor_tab, text="Add New Liquor Item", font=("Helvetica", 14, "bold")).pack(pady=10)
    name_entry = tb.Entry(liquor_tab, width=40)
    name_entry.insert(0, "Item Name")
    name_entry.pack(pady=5)

    category_combo = tb.Combobox(liquor_tab, values=["Wine", "Beer", "Rum", "Whiskey", "Scotch", "Cocktail"])
    category_combo.set("Select Category")
    category_combo.pack(pady=5)

    qty_combo = tb.Combobox(liquor_tab, values=["30ml", "60ml", "90ml", "180ml"])
    qty_combo.set("Select Quantity")
    qty_combo.pack(pady=5)

    mrp_entry = tb.Entry(liquor_tab, width=40)
    mrp_entry.insert(0, "Enter MRP")
    mrp_entry.pack(pady=5)

    liquor_stock_entry = stock_entry_widget(liquor_tab)

    def add_liquor():
        name = name_entry.get().strip()
        category = category_combo.get()
        qty = qty_combo.get()
        try:
            mrp = float(mrp_entry.get())
            stock = int(liquor_stock_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid MRP and stock quantity.")
            return

        if name and category != "Select Category" and qty != "Select Quantity":
            add_menu_item(name, category, "Liquor", qty, mrp, stock)
            messagebox.showinfo("Success", f"{name} ({qty}) added with stock {stock}.")
            name_entry.delete(0, 'end')
            mrp_entry.delete(0, 'end')
            liquor_stock_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Missing Info", "Fill all fields properly.")

    tb.Button(liquor_tab, text="➕ Add Liquor Item", command=add_liquor, bootstyle="success").pack(pady=10)

    # ---------------- Tab 3: Food Menu ---------------- #
    food_tab = tb.Frame(notebook)
    notebook.add(food_tab, text="🍔 Food Menu")

    food_name = tb.Entry(food_tab, width=40)
    food_name.insert(0, "Food Item Name")
    food_name.pack(pady=5)

    food_cat = tb.Combobox(food_tab, values=["Veg", "Non-Veg", "Snacks", "Main Course"])
    food_cat.set("Select Category")
    food_cat.pack(pady=5)

    food_mrp = tb.Entry(food_tab, width=40)
    food_mrp.insert(0, "Enter MRP")
    food_mrp.pack(pady=5)

    def add_food():
        name = food_name.get().strip()
        cat = food_cat.get()
        try:
            mrp = float(food_mrp.get())
        except ValueError:
            messagebox.showerror("Invalid MRP", "Enter valid MRP")
            return

        if name and cat != "Select Category":
            add_menu_item(name, cat, "Food", "plate", mrp, stock=None)  # no stock for food, use raw material model
            messagebox.showinfo("Success", f"{name} added to food menu.")
            food_name.delete(0, 'end')
            food_mrp.delete(0, 'end')
        else:
            messagebox.showwarning("Missing", "Complete all fields")

    tb.Button(food_tab, text="➕ Add Food Item", command=add_food, bootstyle="success").pack(pady=10)

    # ---------------- Tab 4: Beverage Menu ---------------- #
    beverage_tab = tb.Frame(notebook)
    notebook.add(beverage_tab, text="🥤 Beverages")

    bev_name = tb.Entry(beverage_tab, width=40)
    bev_name.insert(0, "Beverage Name")
    bev_name.pack(pady=5)

    bev_cat = tb.Combobox(beverage_tab, values=["Juice", "Soft Drink", "Mocktail", "Energy Drink", "Water Bottle"])
    bev_cat.set("Select Category")
    bev_cat.pack(pady=5)

    bev_mrp = tb.Entry(beverage_tab, width=40)
    bev_mrp.insert(0, "Enter MRP")
    bev_mrp.pack(pady=5)

    beverage_stock_entry = stock_entry_widget(beverage_tab)

    def add_beverage():
        name = bev_name.get().strip()
        cat = bev_cat.get()
        try:
            mrp = float(bev_mrp.get())
            stock = int(beverage_stock_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Enter valid MRP and stock.")
            return

        if name and cat != "Select Category":
            add_menu_item(name, cat, "Beverage", "glass", mrp, stock)
            messagebox.showinfo("Success", f"{name} added with stock {stock}.")
            bev_name.delete(0, 'end')
            bev_mrp.delete(0, 'end')
            beverage_stock_entry.delete(0, 'end')
        else:
            messagebox.showwarning("Missing", "Complete all fields")

    tb.Button(beverage_tab, text="➕ Add Beverage", command=add_beverage, bootstyle="success").pack(pady=10)

    # ---------------- Back Button ---------------- #
    tb.Button(win, text="🔙 Back", command=win.destroy, bootstyle="secondary outline").pack(pady=10)


    