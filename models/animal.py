from typing import List, Optional, Dict
from .base import BaseDocument
from .enums import AnimalStatus
from pydantic import Field

class Animal(BaseDocument):
    name: str
    species: str
    status: AnimalStatus = AnimalStatus.HEALTHY
    feeding_times: List[str] = Field(default_factory=list)
    dietary_requirements: Dict = Field(default_factory=dict)
    habitat_preferences: Dict = Field(default_factory=dict)
    habitat_id: Optional[str] = None
    
    class Settings:
        name = "animals"
        indexes = [
            "name",
            "species",
            "status",
            "habitat_id"
        ]