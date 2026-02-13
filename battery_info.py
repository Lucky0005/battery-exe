import subprocess
import os
import re
import tkinter as tk
from tkinter import messagebox

REPORT_PATH = r"C:\battery_report.html"

def generate_report():
    try:
        subprocess.run(
            ["powercfg", "/batteryreport", "/output", REPORT_PATH],
            check=True
        )
    except subprocess.CalledProcessError:
        messagebox.showerror("Chyba", "Spusť program jako administrátor.")
        return False
    return True

def parse_report():
    if not os.path.exists(REPORT_PATH):
        return None, None

    with open(REPORT_PATH, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Najde první dvě hodnoty mWh v části Installed batteries
    values = re.findall(r"(\d{3,6})\s*mWh", content)

    if len(values) >= 2:
        design_cap = int(values[0])
        full_cap = int(values[1])
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

root = tk.Tk()
root.title("Battery Info")
root.geometry("350x200")

btn = tk.Button(root, text="Zobrazit informace o baterii", command=show_info)
btn.pack(pady=20)

result_label = tk.Label(root, text="", justify="left")
result_label.pack()

root.mainloop()