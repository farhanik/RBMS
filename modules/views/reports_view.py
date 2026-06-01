import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.db_connection import run_query


# 4 reports using SQL aggregation
def report_monthly_rent():
    query = """SELECT DATE_FORMAT(payment_date, '%Y-%m') AS month,
               SUM(amount) AS total_collected, COUNT(*) AS num_payments
               FROM Rental_Payments WHERE status = 'Paid'
               GROUP BY month ORDER BY month"""
    return run_query(query, fetch=True) or []


def report_occupancy():
    query = """SELECT status, COUNT(*) AS count,
               ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM Properties), 2) AS percentage
               FROM Properties GROUP BY status"""
    return run_query(query, fetch=True) or []


def report_overdue():
    query = """SELECT p.payment_id, t.full_name AS tenant, pr.address,
               p.amount, p.payment_date
               FROM Rental_Payments p
               JOIN Lease_Agreements l ON p.lease_id = l.lease_id
               JOIN Tenants t ON l.tenant_id = t.tenant_id
               JOIN Properties pr ON l.property_id = pr.property_id
               WHERE p.status = 'Overdue' ORDER BY p.payment_date"""
    return run_query(query, fetch=True) or []


def report_maintenance_summary():
    query = """SELECT status, COUNT(*) AS num_requests,
               COALESCE(SUM(cost), 0) AS total_cost,
               COALESCE(AVG(cost), 0) AS avg_cost
               FROM Maintenance_Requests GROUP BY status"""
    return run_query(query, fetch=True) or []


def export_csv(rows, default_name):
    if not rows:
        messagebox.showinfo("Export", "No data available to export")
        return
    filename = filedialog.asksaveasfilename(
        defaultextension='.csv',
        filetypes=[('CSV files', '*.csv'), ('All files', '*.*')],
        initialfile=f"{default_name}.csv",
        title="Save Report as CSV"
    )
    if not filename:
        return
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        messagebox.showinfo("Export Successful", f"Report exported to:\n{filename}")
    except Exception as e:
        messagebox.showerror("Export Failed", f"Could not save file:\n{e}")


class ReportsView:
    def __init__(self, parent):
        self.parent = parent
        self.current_data = []
        self.current_report_name = ""
        self.build_ui()

    def build_ui(self):
        
        select_frame = ttk.LabelFrame(self.parent, text="Reports - Click to View", padding=10)
        select_frame.pack(fill='x', padx=10, pady=5)

        ttk.Button(select_frame, text="Monthly Rent Collection",
                   command=lambda: self.load_report(report_monthly_rent(), 'monthly_rent_collection', 'Monthly Rent Collection')).pack(side='left', padx=3)
        ttk.Button(select_frame, text="Property Occupancy",
                   command=lambda: self.load_report(report_occupancy(), 'property_occupancy', 'Property Occupancy')).pack(side='left', padx=3)
        ttk.Button(select_frame, text="Overdue Payments",
                   command=lambda: self.load_report(report_overdue(), 'overdue_payments', 'Overdue Payments')).pack(side='left', padx=3)
        ttk.Button(select_frame, text="Maintenance Summary",
                   command=lambda: self.load_report(report_maintenance_summary(), 'maintenance_summary', 'Maintenance Summary')).pack(side='left', padx=3)

        # Big Export to CSV button at the right side of the buttons
        self.export_btn = ttk.Button(select_frame, text="Export to CSV",
                                      command=self.do_export, state='disabled')
        self.export_btn.pack(side='right', padx=10)

        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Using grid for equal-width left/right columns
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        data_frame = ttk.LabelFrame(main_frame, text="Report Data", padding=5)
        data_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))

        self.report_title = ttk.Label(data_frame, text="Select a report above to view data",
                                       font=('Segoe UI', 10, 'italic'), foreground='#595959')
        self.report_title.pack(anchor='w', pady=(0, 5))

        tree_container = ttk.Frame(data_frame)
        tree_container.pack(fill='both', expand=True)

        self.tree = ttk.Treeview(tree_container, show='headings')
        vsb = ttk.Scrollbar(tree_container, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        tree_container.rowconfigure(0, weight=1)
        tree_container.columnconfigure(0, weight=1)

        # Hint text at bottom of left panel
        ttk.Label(data_frame,
                  text="Tip: Click a report button above, then click 'Export to CSV' to save",
                  font=('Segoe UI', 9, 'italic'), foreground='#595959').pack(anchor='w', pady=(5, 0))

        
        chart_frame = ttk.LabelFrame(main_frame, text="Data Visualisation (Live from Database)", padding=5)
        chart_frame.grid(row=0, column=1, sticky='nsew', padx=(5, 0))

        # Two charts stacked vertically
        chart_frame.rowconfigure(0, weight=1)
        chart_frame.rowconfigure(1, weight=1)
        chart_frame.columnconfigure(0, weight=1)

        top_chart = ttk.Frame(chart_frame)
        top_chart.grid(row=0, column=0, sticky='nsew', pady=(0, 5))

        bottom_chart = ttk.Frame(chart_frame)
        bottom_chart.grid(row=1, column=0, sticky='nsew', pady=(5, 0))

        self.draw_rent_chart(top_chart)
        self.draw_status_chart(bottom_chart)

    def load_report(self, data, csv_name, display_name):
        self.current_data = data
        self.current_report_name = csv_name

        self.report_title.config(text=f"Showing: {display_name} ({len(data)} rows)",
                                  foreground='#1F4E79')

        for col in self.tree['columns']:
            self.tree.heading(col, text='')
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not data:
            self.tree['columns'] = ('message',)
            self.tree.heading('message', text='No Data')
            self.tree.column('message', width=400)
            self.tree.insert('', 'end', values=('No data available for this report',))
            self.export_btn.config(state='disabled')
            return

        headers = list(data[0].keys())
        self.tree['columns'] = headers
        for h in headers:
            self.tree.heading(h, text=h.replace('_', ' ').title())
            self.tree.column(h, width=120, anchor='w')

        for row in data:
            self.tree.insert('', 'end', values=[row[h] for h in headers])

        self.export_btn.config(state='normal')

    def do_export(self):
        if not self.current_data:
            messagebox.showwarning("No Data", "Please load a report first")
            return
        export_csv(self.current_data, self.current_report_name)

    def draw_rent_chart(self, frame):
        data = report_monthly_rent()
        if not data:
            ttk.Label(frame, text="No payment data available").pack(pady=20)
            return
        months = [r['month'] for r in data]
        totals = [float(r['total_collected']) for r in data]

        fig, ax = plt.subplots(figsize=(5, 3), dpi=80)
        ax.bar(months, totals, color='#1F4E79')
        ax.set_title('Monthly Rent Collection', fontsize=11, fontweight='bold', pad=8)
        ax.set_xlabel('Month', fontsize=9)
        ax.set_ylabel('Total Collected ($)', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=8)
        plt.setp(ax.get_yticklabels(), fontsize=8)
        fig.subplots_adjust(bottom=0.22, left=0.16, right=0.95, top=0.88)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def draw_status_chart(self, frame):
        data = report_occupancy()
        if not data:
            ttk.Label(frame, text="No property data available").pack(pady=20)
            return
        labels = [r['status'] for r in data]
        counts = [r['count'] for r in data]

        fig, ax = plt.subplots(figsize=(5, 3), dpi=80)
        colors = ['#4CAF50', '#FF9800', '#F44336', '#2196F3']

        wedges, texts, autotexts = ax.pie(
            counts,
            labels=None,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors[:len(labels)],
            pctdistance=0.75,
            textprops={'fontsize': 9, 'color': 'white', 'fontweight': 'bold'}
        )

        ax.set_title('Property Status Distribution', fontsize=11, fontweight='bold', pad=8)

        ax.legend(wedges, [f"{l} ({c})" for l, c in zip(labels, counts)],
                  title="Status", loc='center left',
                  bbox_to_anchor=(1.0, 0.5), fontsize=8, title_fontsize=9)

        fig.subplots_adjust(left=0.05, right=0.68, top=0.88, bottom=0.05)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)