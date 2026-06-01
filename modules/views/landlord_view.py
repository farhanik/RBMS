import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller import landlord_controller


class LandlordView:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        # Form
        form = ttk.LabelFrame(self.parent, text="Landlord Details", padding=10)
        form.pack(fill='x', padx=10, pady=5)

        ttk.Label(form, text="Full Name:").grid(row=0, column=0, sticky='w', pady=3)
        self.name_entry = ttk.Entry(form, width=35)
        self.name_entry.grid(row=0, column=1, padx=5)

        ttk.Label(form, text="Phone:").grid(row=1, column=0, sticky='w', pady=3)
        self.phone_entry = ttk.Entry(form, width=35)
        self.phone_entry.grid(row=1, column=1, padx=5)

        ttk.Label(form, text="Email:").grid(row=2, column=0, sticky='w', pady=3)
        self.email_entry = ttk.Entry(form, width=35)
        self.email_entry.grid(row=2, column=1, padx=5)

        ttk.Label(form, text="Address:").grid(row=3, column=0, sticky='w', pady=3)
        self.address_entry = ttk.Entry(form, width=35)
        self.address_entry.grid(row=3, column=1, padx=5)

        # Buttons
        btns = ttk.Frame(self.parent)
        btns.pack(pady=5)
        ttk.Button(btns, text="Add", command=self.add).pack(side='left', padx=3)
        ttk.Button(btns, text="Update", command=self.update).pack(side='left', padx=3)
        ttk.Button(btns, text="Delete", command=self.delete).pack(side='left', padx=3)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side='left', padx=3)

        # Search
        search = ttk.Frame(self.parent)
        search.pack(fill='x', padx=10, pady=5)
        ttk.Label(search, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(search, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search, text="Search", command=self.do_search).pack(side='left')
        ttk.Button(search, text="Show All", command=self.refresh_table).pack(side='left', padx=3)

        # Table
        cols = ('ID', 'Name', 'Phone', 'Email', 'Address')
        self.tree = ttk.Treeview(self.parent, columns=cols, show='headings', height=12)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def get_form(self):
        return (self.name_entry.get().strip(), self.phone_entry.get().strip(),
                self.email_entry.get().strip(), self.address_entry.get().strip())

    def validate(self, values):
        for v in values:
            if not v:
                messagebox.showwarning("Validation", "All fields are required")
                return False
        return True

    def add(self):
        values = self.get_form()
        if not self.validate(values):
            return
        result = landlord_controller.add_landlord(*values)
        if result:
            messagebox.showinfo("Success", "Landlord added")
            self.clear()
            self.refresh_table()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a landlord first")
            return
        values = self.get_form()
        if not self.validate(values):
            return
        if not messagebox.askyesno("Confirm", "Update this landlord?"):
            return
        landlord_controller.update_landlord(self.selected_id, *values)
        messagebox.showinfo("Success", "Landlord updated")
        self.clear()
        self.refresh_table()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a landlord first")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure? This cannot be undone."):
            return
        ok, msg = landlord_controller.delete_landlord(self.selected_id)
        if ok:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
        self.clear()
        self.refresh_table()

    def do_search(self):
        kw = self.search_entry.get().strip()
        if not kw:
            self.refresh_table()
            return
        rows = landlord_controller.search_landlords(kw)
        self.populate(rows)

    def refresh_table(self):
        rows = landlord_controller.get_all_landlords()
        self.populate(rows)

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['landlord_id'], r['full_name'],
                                                  r['phone'], r['email'], r['address']))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])['values']
        self.selected_id = vals[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, vals[1])
        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, vals[2])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, vals[3])
        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, vals[4])

    def clear(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.selected_id = None
