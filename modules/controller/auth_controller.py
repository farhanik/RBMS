import hashlib
from database.db_connection import run_query


def hash_password(password):
    # Here simple SHA256 hash with salt
    salt = "realestate_salt_2026"
    return hashlib.sha256((password + salt).encode()).hexdigest()


def login_user(username, password):
    pwd_hash = hash_password(password)
    query = "SELECT * FROM Users WHERE username = %s AND password_hash = %s"
    result = run_query(query, (username, pwd_hash), fetch=True)
    if result:
        return result[0]
    return None


def setup_default_users():
    # Setting up admin and manager passwords on first run
    admin_hash = hash_password("admin123")
    manager_hash = hash_password("manager123")
    run_query("UPDATE Users SET password_hash = %s WHERE username = %s",
              (admin_hash, 'admin'))
    run_query("UPDATE Users SET password_hash = %s WHERE username = %s",
              (manager_hash, 'manager1'))
