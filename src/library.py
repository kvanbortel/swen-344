from src.swen344_db_utils import *
from psycopg2 import sql

def rebuildTables():
    """Recreate the tables to initialize the db"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS example_table
    """
    create_sql = """
        CREATE TABLE example_table(
            example_col VARCHAR(40)
        )
    """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def countRows(table):
    count, = exec_get_one(
        sql.SQL("SELECT count(*) FROM {table}").format(table=sql.Identifier(table))
    )
    return count

