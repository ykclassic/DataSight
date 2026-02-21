from pydantic import BaseModel
from typing import Dict, Any

class UploadResponse(BaseModel):
    schema: Dict[str, Any]
    profile: Dict[str, Any]
