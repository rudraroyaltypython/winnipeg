import ttkbootstrap as tb
from models.order import get_all_active_orders

def open_kitchen_panel(root):
    win = tb.Toplevel(root)
    win.title("🔥 Live Kitchen Panel")
    win.geometry("600x500")

    tree = tb.Treeview(win, columns=("Table", "Items"), show="headings")
    tree.heading("Table", text="Table No.")
    tree.heading("Items", text="Ordered Items")
    tree.pack(expand=True, fill="both", padx=10, pady=10)

    def refresh():
        tree.delete(*tree.get_children())
        for order in get_all_active_orders():
            items = ", ".join([f"{i['name']} ({i['qty']})" for i in order['items']])
            tree.insert("", "end", values=(order['table_no'], items))
        win.after(3000, refresh)

    refresh()
