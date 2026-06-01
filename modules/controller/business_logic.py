from database.db_connection import run_query


def check_double_booking(property_id, start_date, end_date):
    # Checking if property has overlapping active lease
    query = """SELECT lease_id FROM Lease_Agreements
               WHERE property_id = %s AND status = 'Active'
               AND NOT (end_date < %s OR start_date > %s)"""
    result = run_query(query, (property_id, start_date, end_date), fetch=True)
    return len(result) > 0 if result else False


def can_delete_landlord(landlord_id):
    # Cannot delete landlord if they own properties
    query = "SELECT COUNT(*) AS cnt FROM Properties WHERE landlord_id = %s"
    result = run_query(query, (landlord_id,), fetch=True)
    if result and result[0]['cnt'] > 0:
        return False
    return True


def can_delete_property(property_id):
    # Cannot delete property if it has lease history
    query = "SELECT COUNT(*) AS cnt FROM Lease_Agreements WHERE property_id = %s"
    result = run_query(query, (property_id,), fetch=True)
    if result and result[0]['cnt'] > 0:
        return False
    return True


def can_delete_tenant(tenant_id):
    # Cannot delete tenant if they have lease history
    query = "SELECT COUNT(*) AS cnt FROM Lease_Agreements WHERE tenant_id = %s"
    result = run_query(query, (tenant_id,), fetch=True)
    if result and result[0]['cnt'] > 0:
        return False
    return True


def update_property_status(property_id, new_status):
    # Auto update property status
    query = "UPDATE Properties SET status = %s WHERE property_id = %s"
    return run_query(query, (new_status, property_id))
