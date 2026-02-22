# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from app.api.upload import router as upload_router

import subprocess
import threading

app = FastAPI(title="DataSight Unified Service")

# Enable CORS (safe default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(upload_router, prefix="/api")


@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")


# Start Streamlit in background
def run_streamlit():
    subprocess.run(
        [
            "streamlit",
            "run",
            "app/dashboard.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
        ]
    )


@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=run_streamlit)
    thread.daemon = True
    thread.start()
