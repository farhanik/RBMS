import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller import maintenance_controller


class MaintenanceView:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        form = ttk.LabelFrame(self.parent, text="Maintenance Request Details", padding=10)
        form.pack(fill='x', padx=10, pady=5)

        ttk.Label(form, text="Property ID:").grid(row=0, column=0, sticky='w', pady=3)
        self.prop_entry = ttk.Entry(form, width=15)
        self.prop_entry.grid(row=0, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Tenant ID:").grid(row=1, column=0, sticky='w', pady=3)
        self.tenant_entry = ttk.Entry(form, width=15)
        self.tenant_entry.grid(row=1, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Description:").grid(row=2, column=0, sticky='w', pady=3)
        self.desc_entry = ttk.Entry(form, width=50)
        self.desc_entry.grid(row=2, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Priority:").grid(row=3, column=0, sticky='w', pady=3)
        self.priority_combo = ttk.Combobox(form, values=['Low', 'Medium', 'High', 'Urgent'], width=22)
        self.priority_combo.grid(row=3, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Status:").grid(row=4, column=0, sticky='w', pady=3)
        self.status_combo = ttk.Combobox(form, values=['Open', 'In Progress', 'Completed', 'Cancelled'], width=22)
        self.status_combo.grid(row=4, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Request Date (YYYY-MM-DD):").grid(row=5, column=0, sticky='w', pady=3)
        self.req_date_entry = ttk.Entry(form, width=25)
        self.req_date_entry.grid(row=5, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Completion Date (or leave blank):").grid(row=6, column=0, sticky='w', pady=3)
        self.comp_date_entry = ttk.Entry(form, width=25)
        self.comp_date_entry.grid(row=6, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Cost (or 0):").grid(row=7, column=0, sticky='w', pady=3)
        self.cost_entry = ttk.Entry(form, width=15)
        self.cost_entry.grid(row=7, column=1, padx=5, sticky='w')

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

        cols = ('ID', 'Property', 'Tenant', 'Description', 'Priority', 'Status', 'Req Date', 'Comp Date', 'Cost')
        self.tree = ttk.Treeview(self.parent, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=90)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def get_form(self):
        try:
            comp_date = self.comp_date_entry.get().strip() or None
            cost_str = self.cost_entry.get().strip()
            cost = float(cost_str) if cost_str else None
            return (int(self.prop_entry.get()),
                    int(self.tenant_entry.get()),
                    self.desc_entry.get().strip(),
                    self.priority_combo.get(),
                    self.status_combo.get(),
                    self.req_date_entry.get().strip(),
                    comp_date,
                    cost)
        except ValueError:
            messagebox.showwarning("Validation", "Please enter valid numbers")
            return None

    def add(self):
        values = self.get_form()
        if not values:
            return
        maintenance_controller.add_maintenance(*values)
        messagebox.showinfo("Success", "Request added")
        self.clear()
        self.refresh_table()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a request first")
            return
        values = self.get_form()
        if not values:
            return
        if not messagebox.askyesno("Confirm", "Update this request?"):
            return
        maintenance_controller.update_maintenance(self.selected_id, *values)
        messagebox.showinfo("Success", "Request updated")
        self.clear()
        self.refresh_table()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a request first")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure?"):
            return
        maintenance_controller.delete_maintenance(self.selected_id)
        messagebox.showinfo("Success", "Deleted")
        self.clear()
        self.refresh_table()

    def do_search(self):
        kw = self.search_entry.get().strip()
        if not kw:
            self.refresh_table()
            return
        self.populate(maintenance_controller.search_maintenance(kw))

    def refresh_table(self):
        self.populate(maintenance_controller.get_all_maintenance())

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['request_id'], r['property_id'],
                r['tenant_id'], r['description'], r['priority'], r['status'],
                r['request_date'], r['completion_date'] or '', r['cost'] or ''))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])['values']
        self.selected_id = v[0]
        self.prop_entry.delete(0, tk.END); self.prop_entry.insert(0, v[1])
        self.tenant_entry.delete(0, tk.END); self.tenant_entry.insert(0, v[2])
        self.desc_entry.delete(0, tk.END); self.desc_entry.insert(0, v[3])
        self.priority_combo.set(v[4])
        self.status_combo.set(v[5])
        self.req_date_entry.delete(0, tk.END); self.req_date_entry.insert(0, v[6])
        self.comp_date_entry.delete(0, tk.END); self.comp_date_entry.insert(0, str(v[7]))
        self.cost_entry.delete(0, tk.END); self.cost_entry.insert(0, str(v[8]))

    def clear(self):
        for e in [self.prop_entry, self.tenant_entry, self.desc_entry,
                  self.req_date_entry, self.comp_date_entry, self.cost_entry]:
            e.delete(0, tk.END)
        self.priority_combo.set('')
        self.status_combo.set('')
        self.selected_id = None
