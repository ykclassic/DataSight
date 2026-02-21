# app/services/profile_service.py
import sqlite3
import pandas as pd
import tempfile
from typing import Dict

async def load_sqlite_db(uploaded_file):
    """
    Load uploaded SQLite DB file into a dictionary of DataFrames
    """
    contents = await uploaded_file.read()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    conn = sqlite3.connect(tmp_path)
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    db_data: Dict[str, pd.DataFrame] = {}

    for table in tables["name"]:
        try:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            db_data[table] = df
        except Exception as e:
            db_data[table] = pd.DataFrame({"error": [str(e)]})

    conn.close()
    return db_data

def profile_tables(db_data):
    """
    Generate table profiling safely; returns dictionary
    """
    profiles = {}
    for table_name, df in db_data.items():
        try:
            if df.empty:
                profiles[table_name] = {"info": "Empty table"}
            else:
                profiles[table_name] = df.describe(include="all").to_dict()
        except Exception as e:
            profiles[table_name] = {"error": str(e)}
    return profiles
