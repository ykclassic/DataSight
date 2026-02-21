import sqlite3
import pandas as pd
import tempfile

async def load_sqlite_db(uploaded_file):

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
