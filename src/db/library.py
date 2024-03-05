import os
from .swen344_db_utils import *

def rebuild_tables():
    exec_sql_file('src/db/schema.sql')
    exec_sql_file('src/db/test_data.sql')

def getUsers():
    """
    DB layer call for listing all relevant rows of users table

    Returns:
        A list of tuples of (user id, name, phone, email)"""
    return exec_get_all('SELECT id, name, phone, email FROM users')
