# utils/printing.py
import win32print
import win32ui
from datetime import datetime

def print_text(text, printer_name=None):
    # Use default printer if not provided
    if printer_name is None:
        printer_name = win32print.GetDefaultPrinter()

    hPrinter = win32print.OpenPrinter(printer_name)
    hJob = win32print.StartDocPrinter(hPrinter, 1, ("PrintJob", None, "RAW"))
    win32print.StartPagePrinter(hPrinter)
    win32print.WritePrinter(hPrinter, text.encode('utf-8'))
    win32print.EndPagePrinter(hPrinter)
    win32print.EndDocPrinter(hPrinter)
    win32print.ClosePrinter(hPrinter)

def generate_kot_text(table_no, items, kot_no=None, waiter_name=""):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    lines = [
        "======== KOT ========",
        f"Table No: {table_no}",
        f"Time: {timestamp}",
        f"Waiter: {waiter_name}",
        "---------------------"
    ]
    for item in items:
        lines.append(f"{item['qty']} x {item['name']}")
    lines.append("=====================")
    return "\n".join(lines)

def generate_bill_text(table_no, items, service_charge=0, tax=0, discount=0):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
    total = sum(i['qty'] * i['price'] for i in items)
    sc_amt = (service_charge / 100) * total
    tax_amt = (tax / 100) * total
    final_total = total + sc_amt + tax_amt - discount

    lines = [
        "==== Final Bill ====",
        f"Table: {table_no}",
        f"Time: {timestamp}",
        "---------------------",
    ]
    for i in items:
        lines.append(f"{i['qty']} x {i['name']} @ {i['price']}")

    lines.append("---------------------")
    lines.append(f"Subtotal: ₹{total:.2f}")
    if service_charge > 0:
        lines.append(f"Service Charge: ₹{sc_amt:.2f}")
    if tax > 0:
        lines.append(f"Tax: ₹{tax_amt:.2f}")
    if discount > 0:
        lines.append(f"Discount: ₹{discount:.2f}")
    lines.append(f"Total: ₹{final_total:.2f}")
    lines.append("=====================")
    return "\n".join(lines)
