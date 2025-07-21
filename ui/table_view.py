import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from models.menu import get_all_menu_items, update_stock, get_stock
from models.order import create_order, get_order_by_table, finalize_order
from models.tables import set_table_status
from utils.printing import generate_kot_text, generate_bill_text, print_text
from bson import ObjectId
import winsound
from playsound import playsound

order_data = {}

def open_table_window(root, table_no, table_button=None):
    win = tb.Toplevel(root)
    win.title(f"Table {table_no} - Order Details")
    win.geometry("700x600")

    tb.Label(win, text=f"🪑 Table {table_no} Order Summary", font=("Helvetica", 16), bootstyle="primary").pack(pady=10)

    menu_items = get_all_menu_items()
    menu_names = [item['item_name'] for item in menu_items]

    selection_frame = tb.Frame(win)
    selection_frame.pack(pady=10)

    tb.Label(selection_frame, text="Item").grid(row=0, column=0)
    item_var = tb.StringVar()
    item_cb = tb.Combobox(selection_frame, textvariable=item_var, values=menu_names, width=30)
    item_cb.grid(row=0, column=1, padx=5)

    tb.Label(selection_frame, text="Qty").grid(row=0, column=2)
    qty_var = tb.IntVar(value=1)
    qty_entry = tb.Entry(selection_frame, textvariable=qty_var, width=5)
    qty_entry.grid(row=0, column=3, padx=5)

    full_order_items = []   # All items (loaded + session)
    session_items = []      # New items in current session

    def add_item_to_order():
        item_name = item_var.get()
        qty = qty_var.get()
        if not item_name or qty <= 0:
            return

        item = next((i for i in menu_items if i["item_name"] == item_name), None)
        if item:
            session_items.append({
                "name": item_name,
                "qty": qty,
                "price": item["mrp"]
            })
            full_order_items.append({
                "name": item_name,
                "qty": qty,
                "price": item["mrp"]
            })
            refresh_tree()

    tb.Button(selection_frame, text="Add", command=add_item_to_order, bootstyle="success").grid(row=0, column=4, padx=5)

    tree = tb.Treeview(win, columns=("Item", "Qty", "Price"), show="headings", height=10)
    tree.heading("Item", text="Item")
    tree.heading("Qty", text="Qty")
    tree.heading("Price", text="Price")
    tree.pack(pady=10)

    def refresh_tree():
        for i in tree.get_children():
            tree.delete(i)
        for item in full_order_items:
            tree.insert("", "end", values=(item["name"], item["qty"], item["price"]))

    # Load existing order
    existing_order = get_order_by_table(table_no)
    if existing_order:
        for item in existing_order['items']:
            full_order_items.append(item)
        refresh_tree()

    btn_frame = tb.Frame(win)
    btn_frame.pack(pady=10)

    def save_and_print_kot():
        if not session_items:
            Messagebox.show_warning("No new items to print.", "Warning")
            return

        # Stock check
        for item in session_items:
            available = get_stock(item["name"])
            if item["qty"] > available:
                Messagebox.show_error(
                    f"Insufficient stock for '{item['name']}' (Available: {available})",
                    "Stock Alert"
                )
                return

        order_id = create_order(table_no, session_items)

        for item in session_items:
            update_stock(item["name"], item["qty"])

        set_table_status(table_no, "occupied")

        kot_text = generate_kot_text(table_no, session_items)
        print_text(kot_text)

        Messagebox.show_info("KOT Generated", f"KOT for Table {table_no} saved.\nOrder ID: {order_id}")
        playsound("C:/Users/DELL/Desktop/winnipeg v2/bar_restaurant_billing/kot.mp3")
        
        session_items.clear()
        refresh_tree()

        # ✅ Change the color of the table button to red
        if table_button:
            table_button.config(bootstyle="danger")

    def print_bill():
        total = sum(item['qty'] * item['price'] for item in full_order_items)
        Messagebox.show_info("Bill", f"Total Bill: ₹{total:.2f}")
        bill_text = generate_bill_text(table_no, full_order_items, tax=5, service_charge=5)
        print_text(bill_text)

    def finalize_and_close_table():
        finalize_order(table_no)
        set_table_status(table_no, "available")
        Messagebox.show_info("Closed", f"Order finalized. Table {table_no} is now available.")
        win.destroy()

        # ✅ Reset button color to green
        if table_button:
            table_button.config(bootstyle="success")

    tb.Button(btn_frame, text="🖨️ Generate KOT", bootstyle="secondary", command=save_and_print_kot).grid(row=0, column=0, padx=10)
    tb.Button(btn_frame, text="🧾 Print Bill", bootstyle="success", command=print_bill).grid(row=0, column=1, padx=10)
    tb.Button(btn_frame, text="✅ Finalize & Close Table", bootstyle="danger", command=finalize_and_close_table).grid(row=0, column=2, padx=10)
