from database.db_connection import run_query
from modules.controller.business_logic import check_double_booking, update_property_status


def get_all_leases():
    return run_query("SELECT * FROM Lease_Agreements ORDER BY lease_id", fetch=True) or []


def add_lease(property_id, tenant_id, start_date, end_date, monthly_rent, bond_amount, status):
    # Check double booking
    if check_double_booking(property_id, start_date, end_date):
        return False, "Property already has an active lease in this period"
    query = """INSERT INTO Lease_Agreements (property_id, tenant_id, start_date,
               end_date, monthly_rent, bond_amount, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    result = run_query(query, (property_id, tenant_id, start_date, end_date,
                                monthly_rent, bond_amount, status))
    # Auto update property status to Leased
    if result and status == 'Active':
        update_property_status(property_id, 'Leased')
    return True, "Lease added"


def update_lease(lease_id, property_id, tenant_id, start_date, end_date, monthly_rent, bond_amount, status):
    query = """UPDATE Lease_Agreements SET property_id=%s, tenant_id=%s, start_date=%s,
               end_date=%s, monthly_rent=%s, bond_amount=%s, status=%s
               WHERE lease_id=%s"""
    result = run_query(query, (property_id, tenant_id, start_date, end_date,
                                monthly_rent, bond_amount, status, lease_id))
    # If lease terminated, make property available again
    if status in ('Terminated', 'Expired'):
        update_property_status(property_id, 'Available')
    return result is not None


def delete_lease(lease_id):
    # Check if lease has payments linked
    payments = run_query("SELECT COUNT(*) AS cnt FROM Rental_Payments WHERE lease_id=%s",
                          (lease_id,), fetch=True)
    if payments and payments[0]['cnt'] > 0:
        return False, "Cannot delete lease with payment history"
    run_query("DELETE FROM Lease_Agreements WHERE lease_id=%s", (lease_id,))
    return True, "Deleted"


def search_leases(keyword):
    query = """SELECT * FROM Lease_Agreements
               WHERE status LIKE %s OR CAST(property_id AS CHAR) LIKE %s"""
    kw = f"%{keyword}%"
    return run_query(query, (kw, kw), fetch=True) or []
