import base64
import io
import sqlite3
import pandas as pd

def parse_uploaded_file(contents, filename):

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # SQLite
    if filename.endswith(".db"):
        conn = sqlite3.connect(":memory:")
        temp_db = io.BytesIO(decoded)

        with open("temp.db", "wb") as f:
            f.write(temp_db.read())

        conn = sqlite3.connect("temp.db")

        tables = pd.read_sql(
            "SELECT name FROM sqlite_master WHERE type='table';",
            conn
        )

        data = {}
        for table in tables['name']:
            df = pd.read_sql(f"SELECT * FROM {table}", conn)
            data[table] = df

        return data

    # CSV
    elif filename.endswith(".csv"):
        df = pd.read_csv(io.StringIO(decoded.decode()))
        return {"data": df}

    # Excel
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(decoded))
        return {"data": df}

    return {}
