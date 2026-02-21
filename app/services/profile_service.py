# app/services/profile_service.py
import sqlite3
import pandas as pd
import tempfile

# -------------------------------
# Load SQLite database
# -------------------------------
async def load_sqlite_db(uploaded_file):
    """
    Reads an uploaded SQLite file and returns a dict of {table_name: DataFrame}
    """
    contents = await uploaded_file.read()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    conn = sqlite3.connect(tmp_path)

    tables = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table';", conn
    )

    db_data = {}
    for table in tables["name"]:
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        db_data[table] = df

    conn.close()
    return db_data

# -------------------------------
# Profile tables
# -------------------------------
def profile_tables(db_data):
    """
    Takes a dict of {table_name: DataFrame} and returns profiling info
    """
    profiles = {}
    for table_name, df in db_data.items():
        # Use pandas describe for numeric + object types
        profiles[table_name] = df.describe(include="all").to_dict()
    return profiles
