import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller import user_controller


class UserView:
    def __init__(self, parent):
        self.parent = parent
        self.selected_id = None
        self.build_ui()
        self.refresh_table()

    def build_ui(self):
        form = ttk.LabelFrame(self.parent, text="User Account Management (Admin Only)", padding=10)
        form.pack(fill='x', padx=10, pady=5)

        ttk.Label(form, text="Username:").grid(row=0, column=0, sticky='w', pady=3)
        self.username_entry = ttk.Entry(form, width=30)
        self.username_entry.grid(row=0, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Password (only for new user):").grid(row=1, column=0, sticky='w', pady=3)
        self.password_entry = ttk.Entry(form, width=30, show='*')
        self.password_entry.grid(row=1, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Role:").grid(row=2, column=0, sticky='w', pady=3)
        self.role_combo = ttk.Combobox(form, values=['Admin', 'Manager'], width=27, state='readonly')
        self.role_combo.grid(row=2, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Email:").grid(row=3, column=0, sticky='w', pady=3)
        self.email_entry = ttk.Entry(form, width=30)
        self.email_entry.grid(row=3, column=1, padx=5, sticky='w')

        ttk.Label(form, text="Full Name:").grid(row=4, column=0, sticky='w', pady=3)
        self.name_entry = ttk.Entry(form, width=30)
        self.name_entry.grid(row=4, column=1, padx=5, sticky='w')

        btns = ttk.Frame(self.parent)
        btns.pack(pady=5)
        ttk.Button(btns, text="Add User", command=self.add).pack(side='left', padx=3)
        ttk.Button(btns, text="Update", command=self.update).pack(side='left', padx=3)
        ttk.Button(btns, text="Reset Password", command=self.reset_pwd).pack(side='left', padx=3)
        ttk.Button(btns, text="Delete", command=self.delete).pack(side='left', padx=3)
        ttk.Button(btns, text="Clear", command=self.clear).pack(side='left', padx=3)

        search = ttk.Frame(self.parent)
        search.pack(fill='x', padx=10, pady=5)
        ttk.Label(search, text="Search:").pack(side='left')
        self.search_entry = ttk.Entry(search, width=30)
        self.search_entry.pack(side='left', padx=5)
        ttk.Button(search, text="Search", command=self.do_search).pack(side='left')
        ttk.Button(search, text="Show All", command=self.refresh_table).pack(side='left', padx=3)

        cols = ('ID', 'Username', 'Role', 'Email', 'Full Name')
        self.tree = ttk.Treeview(self.parent, columns=cols, show='headings', height=10)
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130)
        self.tree.pack(fill='both', expand=True, padx=10, pady=5)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

    def get_form(self):
        return (self.username_entry.get().strip(),
                self.role_combo.get(),
                self.email_entry.get().strip(),
                self.name_entry.get().strip())

    def add(self):
        username, role, email, name = self.get_form()
        password = self.password_entry.get().strip()
        if not all([username, password, role, email, name]):
            messagebox.showwarning("Validation", "All fields are required for a new user")
            return
        user_controller.add_user(username, password, role, email, name)
        messagebox.showinfo("Success", "User account created")
        self.clear()
        self.refresh_table()

    def update(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a user first")
            return
        username, role, email, name = self.get_form()
        if not all([username, role, email, name]):
            messagebox.showwarning("Validation", "Username, role, email, name are required")
            return
        if not messagebox.askyesno("Confirm", "Update this user?"):
            return
        user_controller.update_user(self.selected_id, username, role, email, name)
        messagebox.showinfo("Success", "User updated")
        self.clear()
        self.refresh_table()

    def reset_pwd(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a user first")
            return
        new_pwd = self.password_entry.get().strip()
        if not new_pwd:
            messagebox.showwarning("Validation", "Enter the new password in the Password field")
            return
        if not messagebox.askyesno("Confirm", "Reset this user's password?"):
            return
        user_controller.reset_password(self.selected_id, new_pwd)
        messagebox.showinfo("Success", "Password reset")
        self.password_entry.delete(0, tk.END)

    def delete(self):
        if not self.selected_id:
            messagebox.showwarning("Select", "Please select a user first")
            return
        if not messagebox.askyesno("Confirm Delete", "Delete this user account?"):
            return
        ok, msg = user_controller.delete_user(self.selected_id)
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
        self.populate(user_controller.search_users(kw))

    def refresh_table(self):
        self.populate(user_controller.get_all_users())

    def populate(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert('', 'end', values=(r['user_id'], r['username'],
                r['role'], r['email'], r['full_name']))

    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        v = self.tree.item(sel[0])['values']
        self.selected_id = v[0]
        self.username_entry.delete(0, tk.END); self.username_entry.insert(0, v[1])
        self.role_combo.set(v[2])
        self.email_entry.delete(0, tk.END); self.email_entry.insert(0, v[3])
        self.name_entry.delete(0, tk.END); self.name_entry.insert(0, v[4])
        self.password_entry.delete(0, tk.END)

    def clear(self):
        for e in [self.username_entry, self.password_entry, self.email_entry, self.name_entry]:
            e.delete(0, tk.END)
        self.role_combo.set('')
        self.selected_id = None