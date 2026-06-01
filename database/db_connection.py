import mysql.connector
from tkinter import messagebox


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'NewPass123',
    'database': 'real_estate_pms'
}


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None


def run_query(query, params=None, fetch=False):
    conn = get_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.rowcount
        cursor.close()
        conn.close()
        return result
    except Exception as e:
        messagebox.showerror("Query Error", str(e))
        if conn:
            conn.close()
        return None
