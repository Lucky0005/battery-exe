import subprocess
import os
import re
import tkinter as tk
from tkinter import messagebox

REPORT_PATH = r"C:\battery_report.html"

def generate_report():
    try:
        subprocess.run(["powercfg", "/batteryreport", "/output", REPORT_PATH], check=True)
    except subprocess.CalledProcessError:
        messagebox.showerror("Chyba", "Nepodařilo se vygenerovat battery report.\nSpusť program jako administrátor.")
        return False
    return True

def parse_report():
    if not os.path.exists(REPORT_PATH):
        return None, None

    with open(REPORT_PATH, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    design = re.search(r"Design Capacity.*?(\d+,\d+|\d+)\s*mWh", content)
    full = re.search(r"Full Charge Capacity.*?(\d+,\d+|\d+)\s*mWh", content)

    if design and full:
        design_cap = int(design.group(1).replace(",", ""))
        full_cap = int(full.group(1).replace(",", ""))
        return design_cap, full_cap

    return None, None

def show_info():
    if not generate_report():
        return

    design, full = parse_report()

    if design and full:
        health = round((full / design) * 100, 1)
        result_label.config(
            text=f"Návrhová kapacita: {design} mWh\n"
                 f"Reálná kapacita: {full} mWh\n"
                 f"Zdraví baterie: {health} %"
        )
    else:
        messagebox.showerror("Chyba", "Nepodařilo se načíst data z reportu.")

# GUI
root = tk.Tk()
root.title("Battery Info")
root.geometry("350x200")

btn = tk.Button(root, text="Zobrazit informace o baterii", command=show_info)
btn.pack(pady=20)

result_label = tk.Label(root, text="", justify="left")
result_label.pack()

root.mainloop()