from database.db_connection import run_query


def get_all_maintenance():
    return run_query("SELECT * FROM Maintenance_Requests ORDER BY request_id", fetch=True) or []


def add_maintenance(property_id, tenant_id, description, priority, status, request_date, completion_date, cost):
    query = """INSERT INTO Maintenance_Requests (property_id, tenant_id, description,
               priority, status, request_date, completion_date, cost)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    return run_query(query, (property_id, tenant_id, description, priority,
                              status, request_date, completion_date, cost))


def update_maintenance(request_id, property_id, tenant_id, description, priority,
                       status, request_date, completion_date, cost):
    query = """UPDATE Maintenance_Requests SET property_id=%s, tenant_id=%s,
               description=%s, priority=%s, status=%s, request_date=%s,
               completion_date=%s, cost=%s
               WHERE request_id=%s"""
    return run_query(query, (property_id, tenant_id, description, priority,
                              status, request_date, completion_date, cost, request_id))


def delete_maintenance(request_id):
    run_query("DELETE FROM Maintenance_Requests WHERE request_id=%s", (request_id,))
    return True


def search_maintenance(keyword):
    query = """SELECT * FROM Maintenance_Requests
               WHERE description LIKE %s OR status LIKE %s OR priority LIKE %s"""
    kw = f"%{keyword}%"
    return run_query(query, (kw, kw, kw), fetch=True) or []
