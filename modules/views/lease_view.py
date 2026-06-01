import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller import lease_controller


class LeaseView:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        form = ttk.LabelFrame(self.parent, text="Lease Agreement Details", padding=10)
        form.pack(fill='x', padx=10, pady=5)

        ttk.Label(form, text="Property ID:").grid(row=0, column=0, sticky='w', pady=3)
        self.prop_entry = ttk.Entry(form, width=15)
        self.prop_entry.grid(row=0, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Tenant ID:").grid(row=1, column=0, sticky='w', pady=3)
        self.tenant_entry = ttk.Entry(form, width=15)
        self.tenant_entry.grid(row=1, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='w', pady=3)
        self.start_entry = ttk.Entry(form, width=25)
        self.start_entry.grid(row=2, column=1, padx=5, sticky='w')

        ttk.Label(form, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, sticky='w', pady=3)
        self.end_entry = ttk.Entry(form, width=25)
        self.end_entry.grid(row=3, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Monthly Rent:").grid(row=4, column=0, sticky='w', pady=3)
        self.rent_entry = ttk.Entry(form, width=15)
        self.rent_entry.grid(row=4, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Bond Amount:").grid(row=5, column=0, sticky='w', pady=3)
        self.bond_entry = ttk.Entry(form, width=15)
        self.bond_entry.grid(row=5, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Status:").grid(row=6, column=0, sticky='w', pady=3)
        self.status_combo = ttk.Combobox(form, values=['Active', 'Expired', 'Terminated'], width=22)
        self.status_combo.grid(row=6, column=1, padx=5, sticky='w')

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

        cols = ('ID', 'Property', 'Tenant', 'Start', 'End', 'Rent', 'Bond', 'Status')
        self.tree = ttk.Treeview(self.parent, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def get_form(self):
        try:
            return (int(self.prop_entry.get()),
                    int(self.tenant_entry.get()),
                    self.start_entry.get().strip(),
                    self.end_entry.get().strip(),
                    float(self.rent_entry.get()),
                    float(self.bond_entry.get()),
                    self.status_combo.get())
        except ValueError:
            messagebox.showwarning("Validation", "Please enter valid numbers")
            return None

    def add(self):
        values = self.get_form()
        if not values:
            return
        ok, msg = lease_controller.add_lease(*values)
        if ok:
            messagebox.showinfo("Success", msg)
        else:
            messagebox.showerror("Error", msg)
        self.clear()
        self.refresh_table()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a lease first")
            return
        values = self.get_form()
        if not values:
            return
        if not messagebox.askyesno("Confirm", "Update this lease?"):
            return
        lease_controller.update_lease(self.selected_id, *values)
        messagebox.showinfo("Success", "Lease updated")
        self.clear()
        self.refresh_table()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a lease first")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure?"):
            return
        ok, msg = lease_controller.delete_lease(self.selected_id)
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
        self.populate(lease_controller.search_leases(kw))

    def refresh_table(self):
        self.populate(lease_controller.get_all_leases())

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['lease_id'], r['property_id'],
                r['tenant_id'], r['start_date'], r['end_date'],
                r['monthly_rent'], r['bond_amount'], r['status']))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])['values']
        self.selected_id = v[0]
        self.prop_entry.delete(0, tk.END); self.prop_entry.insert(0, v[1])
        self.tenant_entry.delete(0, tk.END); self.tenant_entry.insert(0, v[2])
        self.start_entry.delete(0, tk.END); self.start_entry.insert(0, v[3])
        self.end_entry.delete(0, tk.END); self.end_entry.insert(0, v[4])
        self.rent_entry.delete(0, tk.END); self.rent_entry.insert(0, v[5])
        self.bond_entry.delete(0, tk.END); self.bond_entry.insert(0, v[6])
        self.status_combo.set(v[7])

    def clear(self):
        for e in [self.prop_entry, self.tenant_entry, self.start_entry,
                  self.end_entry, self.rent_entry, self.bond_entry]:
            e.delete(0, tk.END)
        self.status_combo.set('')
        self.selected_id = None
