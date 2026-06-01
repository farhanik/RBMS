from database.db_connection import run_query
from modules.controller.business_logic import can_delete_landlord


def get_all_landlords():
    return run_query("SELECT * FROM Landlords ORDER BY landlord_id", fetch=True) or []


def add_landlord(full_name, phone, email, address):
    query = """INSERT INTO Landlords (full_name, phone, email, address)
               VALUES (%s, %s, %s, %s)"""
    return run_query(query, (full_name, phone, email, address))


def update_landlord(landlord_id, full_name, phone, email, address):
    query = """UPDATE Landlords SET full_name=%s, phone=%s, email=%s, address=%s
               WHERE landlord_id=%s"""
    return run_query(query, (full_name, phone, email, address, landlord_id))


def delete_landlord(landlord_id):
    if not can_delete_landlord(landlord_id):
        return False, "Cannot delete landlord who owns properties"
    result = run_query("DELETE FROM Landlords WHERE landlord_id=%s", (landlord_id,))
    return True, "Deleted"


def search_landlords(keyword):
    query = """SELECT * FROM Landlords
               WHERE full_name LIKE %s OR email LIKE %s OR phone LIKE %s"""
    kw = f"%{keyword}%"
    return run_query(query, (kw, kw, kw), fetch=True) or []
