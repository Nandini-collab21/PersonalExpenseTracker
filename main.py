import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ---------------- DATABASE ----------------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT
)
""")
conn.commit()


# ---------------- FUNCTIONS ----------------

def show_expenses():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)


def add_expense():

    amount = amount_entry.get()
    category = category_combo.get()
    description = description_entry.get()
    date = date_entry.get()

    if amount == "" or category == "":
        messagebox.showerror("Error", "Please fill all required fields")
        return

    cursor.execute(
        "INSERT INTO expenses(amount,category,description,date) VALUES(?,?,?,?)",
        (amount, category, description, date)
    )

    conn.commit()

    show_expenses()

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Expense Added")


def select_item(event):

    selected = tree.focus()

    values = tree.item(selected, "values")

    if values:

        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[1])

        category_combo.set(values[2])

        description_entry.delete(0, tk.END)
        description_entry.insert(0, values[3])

        date_entry.delete(0, tk.END)
        date_entry.insert(0, values[4])


def update_expense():

    selected = tree.focus()

    if selected == "":
        return

    expense_id = tree.item(selected)["values"][0]

    cursor.execute("""
        UPDATE expenses
        SET amount=?,
            category=?,
            description=?,
            date=?
        WHERE id=?
    """,
    (
        amount_entry.get(),
        category_combo.get(),
        description_entry.get(),
        date_entry.get(),
        expense_id
    ))

    conn.commit()

    show_expenses()

    messagebox.showinfo("Updated", "Expense Updated")


def delete_expense():

    selected = tree.focus()

    if selected == "":
        return

    expense_id = tree.item(selected)["values"][0]

    cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()

    show_expenses()

    messagebox.showinfo("Deleted", "Expense Deleted")


# ---------------- GUI ----------------

root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("950x650")
root.configure(bg="white")

title = tk.Label(
    root,
    text="Personal Expense Tracker",
    font=("Arial",22,"bold"),
    bg="white",
    fg="blue"
)
title.pack(pady=10)

# Amount

tk.Label(root,text="Amount",bg="white").pack()

amount_entry=tk.Entry(root,width=35)
amount_entry.pack()

# Category

tk.Label(root,text="Category",bg="white").pack()

category_combo=ttk.Combobox(root,width=32)

category_combo["values"]=(
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Entertainment",
    "Health",
    "Education",
    "Other"
)

category_combo.pack()

# Description

tk.Label(root,text="Description",bg="white").pack()

description_entry=tk.Entry(root,width=35)
description_entry.pack()

# Date

tk.Label(root,text="Date",bg="white").pack()

date_entry=tk.Entry(root,width=35)
date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
date_entry.pack()

# Buttons

frame=tk.Frame(root,bg="white")
frame.pack(pady=15)

tk.Button(frame,text="Add Expense",bg="green",fg="white",
          command=add_expense,width=15).grid(row=0,column=0,padx=5)

tk.Button(frame,text="Update",bg="orange",fg="white",
          command=update_expense,width=15).grid(row=0,column=1,padx=5)

tk.Button(frame,text="Delete",bg="red",fg="white",
          command=delete_expense,width=15).grid(row=0,column=2,padx=5)

# Table

columns=("ID","Amount","Category","Description","Date")

tree=ttk.Treeview(root,columns=columns,show="headings",height=12)

for col in columns:
    tree.heading(col,text=col)
    tree.column(col,width=150)

tree.pack(pady=20)

tree.bind("<ButtonRelease-1>",select_item)

show_expenses()

root.mainloop()

conn.close()