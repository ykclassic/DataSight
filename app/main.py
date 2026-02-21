from fastapi import FastAPI
from app.api.upload import router as upload_router
from config.settings import settings

app = FastAPI(title=settings.APP_NAME)

app.include_router(upload_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "running"}
