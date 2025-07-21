# main.py

import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk
from models.tables import get_all_tables, initialize_tables
from ui.table_view import open_table_window
from ui.settings_view import open_menu_settings
from ui.inventory_view import open_inventory_window
from ui.kitchen_panel import open_kitchen_panel


class BarBillingApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Dark mode

        self.title("🍷 Bar & Restaurant Billing System")
        self.state("zoomed")  # Fullscreen window

        # App Title
        tb.Label(
            self,
            text="🍽️ Welcome to Bar & Restaurant Dashboard",
            font=("Helvetica", 24, "bold"),
            bootstyle="info"
        ).pack(pady=20)

        # Scrollable Table Frame
        container = tb.Frame(self)
        container.pack(expand=True, fill=BOTH, padx=20, pady=10)

        canvas = tb.Canvas(container)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = tb.Scrollbar(container, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.table_frame = tb.Frame(canvas)
        canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        # Generate Table Buttons
        self.create_table_grid()
        self.refresh_table_grid()  # Start the auto-refresh loop

        # Settings Button
        tb.Button(
            self,
            text="⚙️ Menu & Table Settings",
            bootstyle="secondary",
            command=lambda: open_menu_settings(self)
        ).pack(pady=20)

        # Inventory Dashboard Button
        tb.Button(
            self,
            text="📦 Inventory Dashboard",
            bootstyle="info",
            command=lambda: open_inventory_window(self)
        ).pack(pady=10)

        tb.Button(
            self,
            text="👨‍🍳 Kitchen Panel",
            bootstyle="warning",
            command=lambda: open_kitchen_panel(self)
        ).pack(pady=10)

    def refresh_table_grid(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.create_table_grid()
        self.after(5000, self.refresh_table_grid)  # auto-refresh every 5 seconds

    def create_table_grid(self):
        tables = get_all_tables()
        cols = 5
        for index, table in enumerate(tables):
            r, c = divmod(index, cols)
            status = table.get("status", "available")
            color = "success" if status == "available" else "danger"

            # Each button needs to be individually passed to open_table_window
            btn = tb.Button(
                self.table_frame,
                text=f"Table {table['table_no']}",
                width=20,
                bootstyle=color
            )
            btn.grid(row=r, column=c, padx=10, pady=10)
            btn.configure(command=lambda b=btn, t=table['table_no']: open_table_window(self, t, table_button=b))


if __name__ == "__main__":
    initialize_tables(total=30)
    app = BarBillingApp()
    app.mainloop()
