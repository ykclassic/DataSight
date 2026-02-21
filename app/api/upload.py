# app/api/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import sqlite3
import pandas as pd
from io import BytesIO

# Services
from app.services.schema_service import analyze_schema
from app.services.profile_service import profile_tables
from app.services.insight_service import generate_insights

router = APIRouter()

async def load_sqlite_db(file: UploadFile):
    """
    Load an uploaded SQLite .db file into a dict of DataFrames.
    """
    contents = await file.read()
    db_dict = {}

    # Use in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    with conn:
        conn.executescript(contents.decode(errors="ignore"))  # For .sql, optional
    try:
        # Standard approach for .db file
        conn = sqlite3.connect(BytesIO(contents))
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table_name_tuple in tables:
            table_name = table_name_tuple[0]
            df = pd.read_sql_query(f"SELECT * FROM '{table_name}'", conn)
            db_dict[table_name] = df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read DB file: {e}")
    finally:
        conn.close()

    return db_dict


@router.post("/upload")
async def upload_databases(files: List[UploadFile] = File(...)):
    """
    Upload one or more SQLite .db files.
    Returns schema, profile, and AI insights (cross-table & trends).
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    results = {}
    db_data_dict = {}

    # Step 1: Load all databases
    for file in files:
        if not file.filename.endswith(".db"):
            raise HTTPException(status_code=400, detail=f"Invalid file type: {file.filename}")

        db_data = await load_sqlite_db(file)
        db_data_dict[file.filename] = db_data

    # Step 2: Schema and profiling per file
    for filename, db_data in db_data_dict.items():
        schema = analyze_schema(db_data)       # Existing schema analysis
        profile = profile_tables(db_data)      # Existing profiling

        results[filename] = {
            "schema": schema,
            "profile": profile
        }

    # Step 3: AI-powered insights (cross-table, trends, correlations)
    ai_insights = generate_insights(db_data_dict)
    results["ai_insights"] = ai_insights

    return results
