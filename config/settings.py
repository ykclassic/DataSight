import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME: str = "AI DB Insight"
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", 50))

settings = Settings()
