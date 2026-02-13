import subprocess
import os
import re
import tkinter as tk
from tkinter import messagebox

REPORT_PATH = os.path.join(os.environ["USERPROFILE"], "battery_report.html")

def generate_report():
    try:
        subprocess.run(
            ["powercfg", "/batteryreport", "/output", REPORT_PATH],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except:
        messagebox.showerror("Chyba", "Spusť program jako administrátor.")
        return False
    return True

def parse_report():
    if not os.path.exists(REPORT_PATH):
        return None, None

    with open(REPORT_PATH, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Najdi sekci Installed batteries
    section = re.search(r"Installed batteries.*?</table>", content, re.DOTALL)

    if not section:
        return None, None

    numbers = re.findall(r"(\d{4,6})\s*mWh", section.group())

    if len(numbers) >= 2:
        design = int(numbers[0])
        full = int(numbers[1])
        return design, full

    return None, None

def show_info():
    btn.config(state="disabled")
    root.update()

    if not generate_report():
        btn.config(state="normal")
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

    btn.config(state="normal")

root = tk.Tk()
root.title("Battery Info")
root.geometry("360x200")

btn = tk.Button(root, text="Zobrazit informace o baterii", command=show_info)
btn.pack(pady=20)

result_label = tk.Label(root, text="", justify="left")
result_label.pack()

root.mainloop()
