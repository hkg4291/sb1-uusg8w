from typing import List, Dict
from .base import BaseDocument
from pydantic import Field

class Habitat(BaseDocument):
    name: str
    type: str
    capacity: int
    features: Dict = Field(default_factory=dict)
    current_conditions: Dict = Field(default_factory=dict)
    
    class Settings:
        name = "habitats"
        indexes = [
            "name",
            "type"
        ]