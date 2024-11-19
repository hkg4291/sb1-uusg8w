from typing import Optional
from datetime import datetime
from .base import BaseDocument
from pydantic import Field

class Note(BaseDocument):
    content: str
    employee_id: str
    animal_id: Optional[str] = None
    habitat_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "notes"
        indexes = [
            "employee_id",
            "animal_id",
            "habitat_id"
        ]