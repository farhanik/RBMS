from database.db_connection import run_query


def get_all_payments():
    return run_query("SELECT * FROM Rental_Payments ORDER BY payment_id", fetch=True) or []


def add_payment(lease_id, amount, payment_date, payment_method, status, notes):
    query = """INSERT INTO Rental_Payments (lease_id, amount, payment_date,
               payment_method, status, notes)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    return run_query(query, (lease_id, amount, payment_date, payment_method, status, notes))


def update_payment(payment_id, lease_id, amount, payment_date, payment_method, status, notes):
    query = """UPDATE Rental_Payments SET lease_id=%s, amount=%s, payment_date=%s,
               payment_method=%s, status=%s, notes=%s
               WHERE payment_id=%s"""
    return run_query(query, (lease_id, amount, payment_date, payment_method,
                              status, notes, payment_id))


def delete_payment(payment_id):
    run_query("DELETE FROM Rental_Payments WHERE payment_id=%s", (payment_id,))
    return True


def search_payments(keyword):
    query = """SELECT * FROM Rental_Payments
               WHERE status LIKE %s OR payment_method LIKE %s OR notes LIKE %s"""
    kw = f"%{keyword}%"
    return run_query(query, (kw, kw, kw), fetch=True) or []
