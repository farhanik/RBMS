import tkinter as tk
from tkinter import ttk, messagebox
from modules.views.login_view import LoginView
from modules.views.landlord_view import LandlordView
from modules.views.property_view import PropertyView
from modules.views.tenant_view import TenantView
from modules.views.lease_view import LeaseView
from modules.views.payment_view import PaymentView
from modules.views.maintenance_view import MaintenanceView
from modules.views.reports_view import ReportsView
from modules.views.user_view import UserView


def apply_styles(root):
    
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass

    PRIMARY = '#1F4E79'

    default_font = ('Segoe UI', 10)
    heading_font = ('Segoe UI', 11, 'bold')

    style.configure('TLabel', font=default_font)
    style.configure('TButton', font=default_font, padding=6)
    style.configure('TEntry', padding=4)
    style.configure('TCombobox', padding=4)
    style.configure('TLabelframe.Label', font=heading_font, foreground=PRIMARY)
    style.configure('Treeview', font=default_font, rowheight=24)
    style.configure('Treeview.Heading', font=heading_font, background=PRIMARY, foreground='white')
    style.configure('TNotebook.Tab', font=default_font, padding=[12, 6])

    style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), foreground=PRIMARY)
    style.configure('SubHeader.TLabel', font=('Segoe UI', 10), foreground='#595959')

    # Logout button
    style.configure('Logout.TButton', font=('Segoe UI', 9, 'bold'),
                    foreground='white', background='#C00000', padding=5)
    style.map('Logout.TButton',
              background=[('active', '#A00000')])


def launch_main_app(user):
    root = tk.Tk()
    root.title("Real Estate Property Management System")
    root.geometry("1280x800")
    root.minsize(1100, 700)

    apply_styles(root)

    # Function to handle logout
    def logout():
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to log out?"):
            root.destroy()
            # Re-open 
            main()

    # Header bar with title, user info, and logout button
    header = ttk.Frame(root, padding=(15, 10, 15, 10))
    header.pack(fill='x')

    title_label = ttk.Label(header, text="Real Estate PMS", style='Header.TLabel')
    title_label.pack(side='left')

    # Logout button on the far right
    logout_btn = ttk.Button(header, text="Logout", command=logout, style='Logout.TButton')
    logout_btn.pack(side='right', padx=5)

    role_badge = "Administrator" if user['role'] == 'Admin' else "Manager"
    user_info = ttk.Label(
        header,
        text=f"Logged in as: {user['full_name']}  |  Role: {role_badge}  |  ",
        style='SubHeader.TLabel'
    )
    user_info.pack(side='right')

    # Separator line
    sep = ttk.Separator(root, orient='horizontal')
    sep.pack(fill='x', padx=15)

    # Main notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=15, pady=10)

    # Tabs visible to everyone
    landlords_tab = ttk.Frame(notebook)
    notebook.add(landlords_tab, text=' Landlords ')
    LandlordView(landlords_tab)

    properties_tab = ttk.Frame(notebook)
    notebook.add(properties_tab, text=' Properties ')
    PropertyView(properties_tab)

    tenants_tab = ttk.Frame(notebook)
    notebook.add(tenants_tab, text=' Tenants ')
    TenantView(tenants_tab)

    leases_tab = ttk.Frame(notebook)
    notebook.add(leases_tab, text=' Lease Agreements ')
    LeaseView(leases_tab)

    payments_tab = ttk.Frame(notebook)
    notebook.add(payments_tab, text=' Rental Payments ')
    PaymentView(payments_tab)

    maint_tab = ttk.Frame(notebook)
    notebook.add(maint_tab, text=' Maintenance ')
    MaintenanceView(maint_tab)

    reports_tab = ttk.Frame(notebook)
    notebook.add(reports_tab, text=' Reports & Charts ')
    ReportsView(reports_tab)

    # ADMIN-ONLY
    if user['role'] == 'Admin':
        users_tab = ttk.Frame(notebook)
        notebook.add(users_tab, text=' User Accounts (Admin) ')
        UserView(users_tab)

    # Status bar
    ttk.Separator(root, orient='horizontal').pack(fill='x', padx=15, side='bottom')
    status_bar = ttk.Frame(root, padding=(15, 5))
    status_bar.pack(fill='x', side='bottom')
    status_text = "Ready  |  ITAP3010 Project  |  VIT Semester 1 2026"
    ttk.Label(status_bar, text=status_text, style='SubHeader.TLabel').pack(side='left')

    root.mainloop()


def main():
    login_root = tk.Tk()
    apply_styles(login_root)
    LoginView(login_root, on_login_success=launch_main_app)
    login_root.mainloop()


if __name__ == "__main__":
    main()