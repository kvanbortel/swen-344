import os
from .swen344_db_utils import *
import hashlib

def rebuild_tables():
    exec_sql_file('src/db/schema.sql')
    exec_sql_file('src/db/test_data.sql')

def getUsers():
    """
    DB layer call for listing all relevant rows of users table

    Returns:
        A list of tuples of (user id, name, phone, email)"""
    return exec_get_all('SELECT id, name, phone, email FROM users')

def isActive(name):
    """Check if an account is active

    Args:
        name: name of a user

    Returns:
        True if the user is active, False otherwise
    """
    is_active, = exec_get_one("""
        SELECT users.active FROM users
        WHERE users.name = %s
    """, (name,))
    return is_active

def hashPassword(password):
    """Hash the given password"""
    hashed_password = hashlib.sha512(password.encode())
    return hashed_password.digest()
