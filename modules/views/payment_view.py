import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller import payment_controller


class PaymentView:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        form = ttk.LabelFrame(self.parent, text="Rental Payment Details", padding=10)
        form.pack(fill='x', padx=10, pady=5)

        ttk.Label(form, text="Lease ID:").grid(row=0, column=0, sticky='w', pady=3)
        self.lease_entry = ttk.Entry(form, width=15)
        self.lease_entry.grid(row=0, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Amount:").grid(row=1, column=0, sticky='w', pady=3)
        self.amount_entry = ttk.Entry(form, width=15)
        self.amount_entry.grid(row=1, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Payment Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='w', pady=3)
        self.date_entry = ttk.Entry(form, width=25)
        self.date_entry.grid(row=2, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Method:").grid(row=3, column=0, sticky='w', pady=3)
        self.method_combo = ttk.Combobox(form, values=['Bank Transfer', 'Cash', 'Card', 'Cheque'], width=22)
        self.method_combo.grid(row=3, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Status:").grid(row=4, column=0, sticky='w', pady=3)
        self.status_combo = ttk.Combobox(form, values=['Paid', 'Pending', 'Overdue'], width=22)
        self.status_combo.grid(row=4, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Notes:").grid(row=5, column=0, sticky='w', pady=3)
        self.notes_entry = ttk.Entry(form, width=40)
        self.notes_entry.grid(row=5, column=1, padx=5, sticky='w')

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

        cols = ('ID', 'Lease', 'Amount', 'Date', 'Method', 'Status', 'Notes')
        self.tree = ttk.Treeview(self.parent, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=110)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def get_form(self):
        try:
            return (int(self.lease_entry.get()),
                    float(self.amount_entry.get()),
                    self.date_entry.get().strip(),
                    self.method_combo.get(),
                    self.status_combo.get(),
                    self.notes_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Validation", "Please enter valid numbers")
            return None

    def add(self):
        values = self.get_form()
        if not values:
            return
        payment_controller.add_payment(*values)
        messagebox.showinfo("Success", "Payment added")
        self.clear()
        self.refresh_table()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a payment first")
            return
        values = self.get_form()
        if not values:
            return
        if not messagebox.askyesno("Confirm", "Update this payment?"):
            return
        payment_controller.update_payment(self.selected_id, *values)
        messagebox.showinfo("Success", "Payment updated")
        self.clear()
        self.refresh_table()

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a payment first")
            return
        if not messagebox.askyesno("Confirm Delete", "Are you sure?"):
            return
        payment_controller.delete_payment(self.selected_id)
        messagebox.showinfo("Success", "Deleted")
        self.clear()
        self.refresh_table()

    def do_search(self):
        kw = self.search_entry.get().strip()
        if not kw:
            self.refresh_table()
            return
        self.populate(payment_controller.search_payments(kw))

    def refresh_table(self):
        self.populate(payment_controller.get_all_payments())

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['payment_id'], r['lease_id'],
                r['amount'], r['payment_date'], r['payment_method'],
                r['status'], r['notes'] or ''))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])['values']
        self.selected_id = v[0]
        self.lease_entry.delete(0, tk.END); self.lease_entry.insert(0, v[1])
        self.amount_entry.delete(0, tk.END); self.amount_entry.insert(0, v[2])
        self.date_entry.delete(0, tk.END); self.date_entry.insert(0, v[3])
        self.method_combo.set(v[4])
        self.status_combo.set(v[5])
        self.notes_entry.delete(0, tk.END); self.notes_entry.insert(0, v[6])

    def clear(self):
        for e in [self.lease_entry, self.amount_entry, self.date_entry, self.notes_entry]:
            e.delete(0, tk.END)
        self.method_combo.set('')
        self.status_combo.set('')
        self.selected_id = None
