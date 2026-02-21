from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.file_service import load_sqlite_db
from app.services.schema_service import analyze_schema
from app.engines.profiling_engine import profile_tables

router = APIRouter()

@router.post("/upload")
async def upload_databases(files: List[UploadFile] = File(...)):

    results = {}

    for file in files:
        if not file.filename.endswith(".db"):
            raise HTTPException(status_code=400, detail="Only .db files allowed")

        db_data = await load_sqlite_db(file)
        schema = analyze_schema(db_data)
        profile = profile_tables(db_data)

        results[file.filename] = {
            "schema": schema,
            "profile": profile
        }

    return results
