from database.db_connection import run_query
from modules.controller.auth_controller import hash_password


def get_all_users():
    return run_query("SELECT user_id, username, role, email, full_name FROM Users ORDER BY user_id", fetch=True) or []


def add_user(username, password, role, email, full_name):
    pwd_hash = hash_password(password)
    query = """INSERT INTO Users (username, password_hash, role, email, full_name)
               VALUES (%s, %s, %s, %s, %s)"""
    return run_query(query, (username, pwd_hash, role, email, full_name))


def update_user(user_id, username, role, email, full_name):
    # Update without changing password
    query = """UPDATE Users SET username=%s, role=%s, email=%s, full_name=%s
               WHERE user_id=%s"""
    return run_query(query, (username, role, email, full_name, user_id))


def reset_password(user_id, new_password):
    pwd_hash = hash_password(new_password)
    query = "UPDATE Users SET password_hash=%s WHERE user_id=%s"
    return run_query(query, (pwd_hash, user_id))


def delete_user(user_id):
    # It Prevent deleting the last admin
    admins = run_query("SELECT COUNT(*) AS cnt FROM Users WHERE role='Admin'", fetch=True)
    user = run_query("SELECT role FROM Users WHERE user_id=%s", (user_id,), fetch=True)
    if user and user[0]['role'] == 'Admin' and admins[0]['cnt'] <= 1:
        return False, "Cannot delete the last Admin user"
    run_query("DELETE FROM Users WHERE user_id=%s", (user_id,))
    return True, "User deleted"


def search_users(keyword):
    query = """SELECT user_id, username, role, email, full_name FROM Users
               WHERE username LIKE %s OR email LIKE %s OR full_name LIKE %s"""
    kw = f"%{keyword}%"
    return run_query(query, (kw, kw, kw), fetch=True) or []