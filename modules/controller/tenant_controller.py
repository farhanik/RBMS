from database.db_connection import run_query
from modules.controller.business_logic import can_delete_tenant


def get_all_tenants():
    return run_query("SELECT * FROM Tenants ORDER BY tenant_id", fetch=True) or []


def add_tenant(full_name, phone, email, emergency_name, emergency_phone, dob):
    query = """INSERT INTO Tenants (full_name, phone, email, emergency_contact_name,
               emergency_contact_phone, date_of_birth)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    return run_query(query, (full_name, phone, email, emergency_name, emergency_phone, dob))


def update_tenant(tenant_id, full_name, phone, email, emergency_name, emergency_phone, dob):
    query = """UPDATE Tenants SET full_name=%s, phone=%s, email=%s,
               emergency_contact_name=%s, emergency_contact_phone=%s, date_of_birth=%s
               WHERE tenant_id=%s"""
    return run_query(query, (full_name, phone, email, emergency_name,
                              emergency_phone, dob, tenant_id))


def delete_tenant(tenant_id):
    if not can_delete_tenant(tenant_id):
        return False, "Cannot delete tenant with lease history"
    run_query("DELETE FROM Tenants WHERE tenant_id=%s", (tenant_id,))
    return True, "Deleted"


def search_tenants(keyword):
    query = """SELECT * FROM Tenants
               WHERE full_name LIKE %s OR email LIKE %s OR phone LIKE %s"""
    kw = f"%{keyword}%"
    return run_query(query, (kw, kw, kw), fetch=True) or []
