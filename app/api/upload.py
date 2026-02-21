# app/api/upload.py
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import asyncio

from app.services.profile_service import load_sqlite_db, profile_tables
from app.engines.insight_engine import analyze_insights  # AI engine from previous phase

router = APIRouter()

@router.post("/upload")
async def upload_databases(files: List[UploadFile]):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    db_data_dict = {}

    # Load all uploaded DB files concurrently
    tasks = [load_sqlite_db(f) for f in files]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for file, result in zip(files, results):
        if isinstance(result, Exception):
            raise HTTPException(status_code=500, detail=f"Failed to read {file.filename}: {result}")
        db_data_dict[file.filename] = result

    # -------------------------------
    # Generate table profiling
    # -------------------------------
    profile_dict = {fname: profile_tables(tables) for fname, tables in db_data_dict.items()}

    # -------------------------------
    # Generate AI insights
    # -------------------------------
    insights = analyze_insights(db_data_dict, predict_future=True)

    # -------------------------------
    # Prepare response
    # -------------------------------
    response = {}
    for fname in db_data_dict.keys():
        response[fname] = {
            "schema": {table: list(df.columns) for table, df in db_data_dict[fname].items()},
            "profile": profile_dict[fname],
            "ai_insights": insights.get(fname, {})
        }

    # Include cross-file relationships
    response["ai_insights"] = {"cross_file_relationships": insights.get("cross_file_relationships", [])}

    return JSONResponse(content=response)
