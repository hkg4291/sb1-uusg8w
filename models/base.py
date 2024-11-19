from datetime import datetime
from typing import Optional, List
from beanie import Document
from pydantic import BaseModel, Field

class BaseDocument(Document):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        use_state_management = True

    async def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super().save(*args, **kwargs)