import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient
import json


def connect_and_insert():
    host = host_entry.get().strip()
    port_text = port_entry.get().strip()
    db_name = db_entry.get().strip()
    collection_name = collection_entry.get().strip()
    key = key_entry.get().strip()
    value_text = value_entry.get().strip()

    if not all([host, port_text, db_name, collection_name, key, value_text]):
        messagebox.showerror("Error", "Please complete all fields.")
        return

    try:
        port = int(port_text)
    except ValueError:
        messagebox.showerror("Invalid Port", "Port must be an integer.")
        return

    try:
        value = json.loads(value_text)
    except Exception:
        value = value_text

    document = {key: value}

    client = None
    try:
        client = MongoClient(host, port, serverSelectionTimeoutMS=5000)
        db = client[db_name]
        col = db[collection_name]
        result = col.insert_one(document)
        messagebox.showinfo("Success", f"Inserted document:\n{json.dumps(document, indent=2)}\n\nInserted id: {result.inserted_id}")
    except Exception as e:
        messagebox.showerror("Connection Error", str(e))
    finally:
        if client is not None:
            try:
                client.close()
            except Exception:
                pass

root = tk.Tk()
root.title("MongoDB Configurator")
root.geometry("480x320")
root.resizable(False, False)

frm = ttk.Frame(root, padding=12)
frm.grid(row=0, column=0, sticky="NSEW")

ttk.Label(frm, text="Host:").grid(row=0, column=0, sticky="W", pady=4)
host_entry = ttk.Entry(frm)
host_entry.insert(0, "localhost")
host_entry.grid(row=0, column=1, sticky="EW", pady=4)

ttk.Label(frm, text="Port:").grid(row=1, column=0, sticky="W", pady=4)
port_entry = ttk.Entry(frm)
port_entry.insert(0, "27017")
port_entry.grid(row=1, column=1, sticky="EW", pady=4)

ttk.Label(frm, text="Database:").grid(row=2, column=0, sticky="W", pady=4)
db_entry = ttk.Entry(frm)
db_entry.grid(row=2, column=1, sticky="EW", pady=4)

ttk.Label(frm, text="Collection:").grid(row=3, column=0, sticky="W", pady=4)
collection_entry = ttk.Entry(frm)
collection_entry.grid(row=3, column=1, sticky="EW", pady=4)

# Document fields
ttk.Label(frm, text="Document key:").grid(row=4, column=0, sticky="W", pady=4)
key_entry = ttk.Entry(frm)
key_entry.grid(row=4, column=1, sticky="EW", pady=4)

ttk.Label(frm, text="Document value (JSON or text):").grid(row=5, column=0, sticky="W", pady=4)
value_entry = ttk.Entry(frm)
value_entry.grid(row=5, column=1, sticky="EW", pady=4)

# Button
insert_btn = ttk.Button(frm, text="Connect and Insert", command=connect_and_insert)
insert_btn.grid(row=6, column=0, columnspan=2, pady=12)

# Make column 1 expand
frm.columnconfigure(1, weight=1)

root.mainloop()
