import tkinter as tk
from tkinter import ttk, messagebox
from database import *

def launch_ui():
    root = tk.Tk()
    root.title("Tookam Management System – 2026")
    root.geometry("800x500")

    ttk.Label(
        root,
        text="Tookam Management System",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    ttk.Button(root, text="Manage Tookakkar", width=30,
               command=lambda: open_tookakkar(root)).pack(pady=5)

    ttk.Button(root, text="Manage Karakkar (10)", width=30,
               command=lambda: open_karakkar(root)).pack(pady=5)

    ttk.Button(root, text="Assign & Order", width=30,
               command=lambda: open_assignment(root)).pack(pady=5)

    ttk.Button(root, text="Export PDF", width=30,
               state="disabled").pack(pady=5)

    root.mainloop()

def open_tookakkar(parent):
    win = tk.Toplevel(parent)
    win.title("Tookakkar")
    win.geometry("600x400")

    ttk.Label(win, text="Name (Malayalam)").grid(row=0, column=0)
    name = ttk.Entry(win, width=30)
    name.grid(row=0, column=1)

    ttype = tk.StringVar(value="തൂക്കാക്കർ")
    ttk.Radiobutton(win, text="തൂക്കാക്കർ", variable=ttype, value="തൂക്കാക്കർ").grid(row=1, column=0)
    ttk.Radiobutton(win, text="തൂക്കാക്കരൻ", variable=ttype, value="തൂക്കാക്കരൻ").grid(row=1, column=1)

    def save():
        if not name.get():
            return
        add_tookakkar(name.get(), ttype.get())
        name.delete(0, tk.END)
        refresh()

    ttk.Button(win, text="Save", command=save).grid(row=2, column=0, columnspan=2)

    tree = ttk.Treeview(win, columns=("id", "name", "type"), show="headings")
    tree.grid(row=3, column=0, columnspan=2, pady=10)

    for c in ("id", "name", "type"):
        tree.heading(c, text=c)

    def refresh():
        tree.delete(*tree.get_children())
        for _, uid, n, t in fetch_tookakkar():
            tree.insert("", "end", values=(uid, n, t))

    refresh()

def open_karakkar(parent):
    win = tk.Toplevel(parent)
    win.title("Karakkar (10)")
    win.geometry("400x450")

    entries = {}
    for i in range(1, 11):
        ttk.Label(win, text=f"Karakkar {i}").grid(row=i, column=0)
        e = ttk.Entry(win, width=25)
        e.grid(row=i, column=1)
        entries[i] = e

    for i, n in fetch_karakkar():
        entries[i].insert(0, n)

    def save_all():
        for i in range(1, 11):
            if not entries[i].get():
                messagebox.showerror("Error", "All 10 required")
                return
        for i in range(1, 11):
            save_karakkar(i, entries[i].get())
        win.destroy()

    ttk.Button(win, text="Save All", command=save_all).grid(row=11, column=0, columnspan=2)

def open_assignment(parent):
    win = tk.Toplevel(parent)
    win.title("Assignment & Order")
    win.geometry("750x450")

    kar = fetch_karakkar()
    tkkr = fetch_tookakkar()

    if not kar or not tkkr:
        messagebox.showerror("Error", "Karakkar & Tookakkar required")
        win.destroy()
        return

    kar_var = tk.StringVar()
    tk_var = tk.StringVar()

    ttk.Combobox(win, textvariable=kar_var,
                 values=[f"{i}-{n}" for i, n in kar]).grid(row=0, column=1)
    ttk.Combobox(win, textvariable=tk_var,
                 values=[f"{i}-{n}" for i, _, n, _ in tkkr]).grid(row=1, column=1)

    ttk.Label(win, text="Karakkar").grid(row=0, column=0)
    ttk.Label(win, text="Tookakkar").grid(row=1, column=0)

    tree = ttk.Treeview(win, columns=("o", "tk", "n", "k"), show="headings")
    tree.grid(row=3, column=0, columnspan=3)

    for c in ("o", "tk", "n", "k"):
        tree.heading(c, text=c)

    def refresh():
        tree.delete(*tree.get_children())
        for r in fetch_assignments():
            tree.insert("", "end", iid=r[0],
                        values=(r[1], r[2], r[3], f"{r[4]}-{r[5]}"))

    def assign():
        if not kar_var.get() or not tk_var.get():
            return
        kar_id = int(kar_var.get().split("-")[0])
        tk_id = int(tk_var.get().split("-")[0])
        add_assignment(kar_id, tk_id, len(fetch_assignments()) + 1)
        refresh()

    ttk.Button(win, text="Assign", command=assign).grid(row=2, column=0, columnspan=2)
    refresh()

