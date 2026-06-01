import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller import tenant_controller


class TenantView:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        form = ttk.LabelFrame(self.parent, text="Tenant Details", padding=10)
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

        ttk.Label(form, text="Emergency Name:").grid(row=3, column=0, sticky='w', pady=3)
        self.emer_name_entry = ttk.Entry(form, width=35)
        self.emer_name_entry.grid(row=3, column=1, padx=5)

        ttk.Label(form, text="Emergency Phone:").grid(row=4, column=0, sticky='w', pady=3)
        self.emer_phone_entry = ttk.Entry(form, width=35)
        self.emer_phone_entry.grid(row=4, column=1, padx=5)

        ttk.Label(form, text="Date of Birth (YYYY-MM-DD):").grid(row=5, column=0, sticky='w', pady=3)
        self.dob_entry = ttk.Entry(form, width=35)
        self.dob_entry.grid(row=5, column=1, padx=5)

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

        cols = ('ID', 'Name', 'Phone', 'Email', 'Emer Name', 'Emer Phone', 'DOB')
        self.tree = ttk.Treeview(self.parent, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def get_form(self):
        return (self.name_entry.get().strip(), self.phone_entry.get().strip(),
                self.email_entry.get().strip(), self.emer_name_entry.get().strip(),
                self.emer_phone_entry.get().strip(), self.dob_entry.get().strip())

    def validate(self, values):
        for v in values:
            if not v:
                messagebox.showwarning("Validation", "All fields required")
                return False
        return True

    def add(self):
        values = self.get_form()
        if not self.validate(values):
            return
        tenant_controller.add_tenant(*values)
        messagebox.showinfo("Success", "Tenant added")
        self.clear()
        self.refresh_table()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a tenant first")
            return
        values = self.get_form()
        if not self.validate(values):
            return
        if not messagebox.askyesno("Confirm", "Update this tenant?"):
            return
        tenant_controller.update_tenant(self.selected_id, *values)
        messagebox.showinfo("Success", "Tenant updated")
        self.clear()
        self.refresh_table()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a tenant first")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure?"):
            return
        ok, msg = tenant_controller.delete_tenant(self.selected_id)
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
        self.populate(tenant_controller.search_tenants(kw))

    def refresh_table(self):
        self.populate(tenant_controller.get_all_tenants())

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['tenant_id'], r['full_name'],
                r['phone'], r['email'], r['emergency_contact_name'],
                r['emergency_contact_phone'], r['date_of_birth']))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])['values']
        self.selected_id = v[0]
        self.name_entry.delete(0, tk.END); self.name_entry.insert(0, v[1])
        self.phone_entry.delete(0, tk.END); self.phone_entry.insert(0, v[2])
        self.email_entry.delete(0, tk.END); self.email_entry.insert(0, v[3])
        self.emer_name_entry.delete(0, tk.END); self.emer_name_entry.insert(0, v[4])
        self.emer_phone_entry.delete(0, tk.END); self.emer_phone_entry.insert(0, v[5])
        self.dob_entry.delete(0, tk.END); self.dob_entry.insert(0, v[6])

    def clear(self):
        for e in [self.name_entry, self.phone_entry, self.email_entry,
                  self.emer_name_entry, self.emer_phone_entry, self.dob_entry]:
            e.delete(0, tk.END)
        self.selected_id = None
