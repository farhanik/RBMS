import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller import property_controller


class PropertyView:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        form = ttk.LabelFrame(self.parent, text="Property Details", padding=10)
        form.pack(fill='x', padx=10, pady=5)

        ttk.Label(form, text="Landlord ID:").grid(row=0, column=0, sticky='w', pady=3)
        self.landlord_entry = ttk.Entry(form, width=20)
        self.landlord_entry.grid(row=0, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Address:").grid(row=1, column=0, sticky='w', pady=3)
        self.address_entry = ttk.Entry(form, width=40)
        self.address_entry.grid(row=1, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Suburb:").grid(row=2, column=0, sticky='w', pady=3)
        self.suburb_entry = ttk.Entry(form, width=25)
        self.suburb_entry.grid(row=2, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Type:").grid(row=3, column=0, sticky='w', pady=3)
        self.type_combo = ttk.Combobox(form, values=['Apartment', 'House', 'Townhouse', 'Studio', 'Unit'], width=22)
        self.type_combo.grid(row=3, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Bedrooms:").grid(row=4, column=0, sticky='w', pady=3)
        self.bedrooms_entry = ttk.Entry(form, width=10)
        self.bedrooms_entry.grid(row=4, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Bathrooms:").grid(row=5, column=0, sticky='w', pady=3)
        self.bathrooms_entry = ttk.Entry(form, width=10)
        self.bathrooms_entry.grid(row=5, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Monthly Rent:").grid(row=6, column=0, sticky='w', pady=3)
        self.rent_entry = ttk.Entry(form, width=15)
        self.rent_entry.grid(row=6, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Status:").grid(row=7, column=0, sticky='w', pady=3)
        self.status_combo = ttk.Combobox(form, values=['Available', 'Leased', 'Maintenance'], width=22)
        self.status_combo.grid(row=7, column=1, padx=5, sticky='w')

        btns = ttk.Frame(self.parent)
        btns.pack(pady=5)
        ttk.Button(btns, text="Add", command=self.add).pack(side='left', padx=3)
        ttk.Button(btns, text="Update", command=self.update).pack(side='left', padx=3)
        ttk.Button(btns, text="Delete", command=self.delete).pack(side='left', padx=3)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side='left', padx=3)

        search = ttk.Frame(self.parent)
        search.pack(fill='x', padx=10, pady=5)
        ttk.Label(search, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(search, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search, text="Search", command=self.do_search).pack(side='left')
        ttk.Button(search, text="Show All", command=self.refresh_table).pack(side='left', padx=3)

        cols = ('ID', 'Landlord', 'Address', 'Suburb', 'Type', 'Beds', 'Baths', 'Rent', 'Status')
        self.tree = ttk.Treeview(self.parent, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def get_form(self):
        try:
            return (int(self.landlord_entry.get()),
                    self.address_entry.get().strip(),
                    self.suburb_entry.get().strip(),
                    self.type_combo.get(),
                    int(self.bedrooms_entry.get()),
                    int(self.bathrooms_entry.get()),
                    float(self.rent_entry.get()),
                    self.status_combo.get())
        except ValueError:
            messagebox.showwarning("Validation", "Please enter valid numbers")
            return None

    def add(self):
        values = self.get_form()
        if not values:
            return
        if not all(values):
            messagebox.showwarning("Validation", "All fields are required")
            return
        property_controller.add_property(*values)
        messagebox.showinfo("Success", "Property added")
        self.clear()
        self.refresh_table()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a property first")
            return
        values = self.get_form()
        if not values:
            return
        if not messagebox.askyesno("Confirm", "Update this property?"):
            return
        property_controller.update_property(self.selected_id, *values)
        messagebox.showinfo("Success", "Property updated")
        self.clear()
        self.refresh_table()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a property first")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure?"):
            return
        ok, msg = property_controller.delete_property(self.selected_id)
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
        self.populate(property_controller.search_properties(kw))

    def refresh_table(self):
        self.populate(property_controller.get_all_properties())

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['property_id'], r['landlord_id'],
                r['address'], r['suburb'], r['property_type'], r['bedrooms'],
                r['bathrooms'], r['monthly_rent'], r['status']))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])['values']
        self.selected_id = v[0]
        self.landlord_entry.delete(0, tk.END); self.landlord_entry.insert(0, v[1])
        self.address_entry.delete(0, tk.END); self.address_entry.insert(0, v[2])
        self.suburb_entry.delete(0, tk.END); self.suburb_entry.insert(0, v[3])
        self.type_combo.set(v[4])
        self.bedrooms_entry.delete(0, tk.END); self.bedrooms_entry.insert(0, v[5])
        self.bathrooms_entry.delete(0, tk.END); self.bathrooms_entry.insert(0, v[6])
        self.rent_entry.delete(0, tk.END); self.rent_entry.insert(0, v[7])
        self.status_combo.set(v[8])

    def clear(self):
        for e in [self.landlord_entry, self.address_entry, self.suburb_entry,
                  self.bedrooms_entry, self.bathrooms_entry, self.rent_entry]:
            e.delete(0, tk.END)
        self.type_combo.set('')
        self.status_combo.set('')
        self.selected_id = None
