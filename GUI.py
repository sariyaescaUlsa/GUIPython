import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pymongo import MongoClient
import json

class MongoGuiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MongoDB GUI Insert Tool")
        self.geometry("600x500")
        
        # --- Connection config section ---
        frame_conn = ttk.LabelFrame(self, text="MongoDB Connection")
        frame_conn.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(frame_conn, text="URI:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.uri_entry = ttk.Entry(frame_conn, width=50)
        self.uri_entry.grid(row=0, column=1, padx=5, pady=5)
        self.uri_entry.insert(0, "mongodb://localhost:27017/")
        
        ttk.Label(frame_conn, text="Database:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.db_entry = ttk.Entry(frame_conn, width=30)
        self.db_entry.grid(row=1, column=1, padx=5, pady=5)
        self.db_entry.insert(0, "testdb")
        
        ttk.Label(frame_conn, text="Collection:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.coll_entry = ttk.Entry(frame_conn, width=30)
        self.coll_entry.grid(row=2, column=1, padx=5, pady=5)
        self.coll_entry.insert(0, "testcoll")
        
        self.connect_button = ttk.Button(frame_conn, text="Connect", command=self.connect_to_mongo)
        self.connect_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Status
        self.status_label = ttk.Label(self, text="Not connected", foreground="red")
        self.status_label.pack(fill="x", padx=10, pady=5)
        
        # --- Document input section ---
        frame_doc = ttk.LabelFrame(self, text="Document to Insert (JSON)")
        frame_doc.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.doc_text = scrolledtext.ScrolledText(frame_doc, height=10)
        self.doc_text.pack(fill="both", expand=True, padx=5, pady=5)
        # put a sample JSON
        self.doc_text.insert("1.0", '{\n    "name": "Alice",\n    "age": 30,\n    "city": "Chihuahua"\n}')
        
        self.insert_button = ttk.Button(self, text="Insert Document", command=self.insert_document, state="disabled")
        self.insert_button.pack(pady=10)
        
        # Internal variables
        self.client = None
        self.db = None
        self.collection = None
    
    def connect_to_mongo(self):
        uri = self.uri_entry.get().strip()
        dbname = self.db_entry.get().strip()
        collname = self.coll_entry.get().strip()
        
        try:
            self.client = MongoClient(uri)
            self.db = self.client[dbname]
            self.collection = self.db[collname]
            # maybe test connection
            _ = self.db.list_collection_names()  # simple operation
            self.status_label.config(text=f"Connected to {dbname}.{collname}", foreground="green")
            self.insert_button.config(state="normal")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to MongoDB: {e}")
            self.status_label.config(text="Connection failed", foreground="red")
            self.insert_button.config(state="disabled")
    
    def insert_document(self):
        text = self.doc_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Needed", "Please enter JSON document.")
            return
        
        try:
            doc = json.loads(text)
        except json.JSONDecodeError as e:
            messagebox.showerror("JSON Error", f"Invalid JSON format: {e}")
            return
        
        try:
            result = self.collection.insert_one(doc)  # single doc insert :contentReference[oaicite:4]{index=4}
            inserted_id = result.inserted_id
            messagebox.showinfo("Success", f"Document inserted, _id = {inserted_id}")
        except Exception as e:
            messagebox.showerror("Insert Error", f"Error inserting document: {e}")
        

if __name__ == "__main__":
    app = MongoGuiApp()
    app.mainloop()
