import tkinter as tk
from tkinter import ttk, messagebox
from modules.controller.auth_controller import login_user


class LoginView:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Real Estate PMS - Login")
        self.root.geometry("400x300")
        self.build_ui()

    def build_ui(self):
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True, fill='both')

        title = ttk.Label(frame, text="Real Estate PMS", font=('Arial', 18, 'bold'))
        title.pack(pady=10)

        subtitle = ttk.Label(frame, text="Please log in", font=('Arial', 11))
        subtitle.pack(pady=5)

        ttk.Label(frame, text="Username:").pack(anchor='w', pady=(15, 2))
        self.username_entry = ttk.Entry(frame, width=30)
        self.username_entry.pack()

        ttk.Label(frame, text="Password:").pack(anchor='w', pady=(10, 2))
        self.password_entry = ttk.Entry(frame, width=30, show='*')
        self.password_entry.pack()

        ttk.Button(frame, text="Login", command=self.do_login, width=20).pack(pady=20)

        info = ttk.Label(frame, text="Default: admin / admin123", font=('Arial', 9), foreground='gray')
        info.pack()

    def do_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Error", "Please enter username and password")
            return

        user = login_user(username, password)
        if user:
            messagebox.showinfo("Success", f"Welcome {user['full_name']}!")
            self.root.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
