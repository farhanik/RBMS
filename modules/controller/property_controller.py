from database.db_connection import run_query
from modules.controller.business_logic import can_delete_property


def get_all_properties():
    return run_query("SELECT * FROM Properties ORDER BY property_id", fetch=True) or []


def add_property(landlord_id, address, suburb, property_type, bedrooms, bathrooms, monthly_rent, status):
    query = """INSERT INTO Properties (landlord_id, address, suburb, property_type,
               bedrooms, bathrooms, monthly_rent, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    return run_query(query, (landlord_id, address, suburb, property_type,
                              bedrooms, bathrooms, monthly_rent, status))


def update_property(property_id, landlord_id, address, suburb, property_type,
                    bedrooms, bathrooms, monthly_rent, status):
    query = """UPDATE Properties SET landlord_id=%s, address=%s, suburb=%s,
               property_type=%s, bedrooms=%s, bathrooms=%s, monthly_rent=%s, status=%s
               WHERE property_id=%s"""
    return run_query(query, (landlord_id, address, suburb, property_type,
                              bedrooms, bathrooms, monthly_rent, status, property_id))


def delete_property(property_id):
    if not can_delete_property(property_id):
        return False, "Cannot delete property with lease history"
    run_query("DELETE FROM Properties WHERE property_id=%s", (property_id,))
    return True, "Deleted"


def search_properties(keyword):
    query = """SELECT * FROM Properties
               WHERE address LIKE %s OR suburb LIKE %s OR property_type LIKE %s"""
    kw = f"%{keyword}%"
    return run_query(query, (kw, kw, kw), fetch=True) or []
