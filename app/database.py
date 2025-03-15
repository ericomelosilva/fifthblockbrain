import sqlite3
import os

DB_NAME = "attendance.db"

def get_connection():
    """
    Returns a connection object to the SQLite database.
    If 'attendance.db' doesn't exist yet, it will be created automatically.
    """
    return sqlite3.connect(DB_NAME)

def create_tables_from_file():
    """
    Reads the SQL script from 'resources/schema.sql' and executes it
    to create (if not exists) all required tables in the database.
    """
    # Get an absolute path to schema.sql
    current_dir = os.path.dirname(__file__)  # the directory where database.py is located
    schema_path = os.path.join(current_dir, "..", "resources", "schema.sql")

    # Read the SQL script
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_script = f.read()

    # Execute the script
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()

def add_ensemble(ensemble_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ensembles (ensemble_name) VALUES (?)", (ensemble_name,))
    conn.commit()
    conn.close()

def get_ensembles():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ensemble_id, ensemble_name FROM ensembles")
    rows = cursor.fetchall()
    conn.close()
    return rows

