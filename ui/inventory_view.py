# ui/inventory_view.py

import csv
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import BOTH, END, filedialog, messagebox
from models.menu import get_all_menu_items, add_menu_item


def open_inventory_window(root):
    win = tb.Toplevel(root)
    win.title("📦 Inventory Dashboard")
    win.geometry("950x550")
    win.grab_set()

    tb.Label(win, text="Inventory Overview", font=("Helvetica", 16, "bold")).pack(pady=10)

    frame = tb.Frame(win)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    cols = ("Item Name", "Category", "Type", "Unit", "Qty Type", "MRP", "Stock Qty")
    tree = tb.Treeview(frame, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, anchor=CENTER, width=120)

    tree.pack(fill=BOTH, expand=True)

    def load_inventory():
        tree.delete(*tree.get_children())
        items = get_all_menu_items()
        for item in items:
            tree.insert("", END, values=(
                item.get("item_name"),
                item.get("category"),
                item.get("type", ""),
                item.get("unit", ""),
                item.get("qty_type", ""),
                f"₹{item.get('mrp', 0):.2f}",
                item.get("stock_qty", 0)
            ))

    def export_to_csv():
        filepath = filedialog.asksaveasfilename(defaultextension=".csv",
                                                filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        try:
            with open(filepath, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(cols)
                for row in tree.get_children():
                    writer.writerow(tree.item(row)['values'])
            messagebox.showinfo("✅ Export Success", "Inventory exported successfully!")
        except Exception as e:
            messagebox.showerror("❌ Export Failed", str(e))

    def import_from_csv():
        filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not filepath:
            return
        try:
            with open(filepath, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    add_menu_item(
                        name=row.get("Item Name"),
                        category=row.get("Category"),
                        item_type=row.get("Type", ""),
                        unit=row.get("Unit", ""),
                        mrp=float(row.get("MRP", 0).replace("₹", "")),
                        stock_qty=int(row.get("Stock Qty", 0))
                    )
            load_inventory()
            messagebox.showinfo("✅ Import Success", "Inventory imported successfully!")
        except Exception as e:
            messagebox.showerror("❌ Import Failed", str(e))

    load_inventory()

    btn_frame = tb.Frame(win)
    btn_frame.pack(pady=10)

    tb.Button(btn_frame, text="🔄 Refresh", command=load_inventory, bootstyle="info").pack(side=LEFT, padx=5)
    tb.Button(btn_frame, text="⬆️ Export to CSV", command=export_to_csv, bootstyle="success").pack(side=LEFT, padx=5)
    tb.Button(btn_frame, text="⬇️ Import from CSV", command=import_from_csv, bootstyle="warning").pack(side=LEFT, padx=5)
    tb.Button(btn_frame, text="⬅️ Back", command=win.destroy, bootstyle="secondary").pack(side=LEFT, padx=5)
