from typing import List, Optional
from app.models.animal import Animal
from app.models.enums import AnimalStatus

class AnimalService:
    @staticmethod
    async def create_animal(name: str, species: str, habitat_id: Optional[str] = None) -> Animal:
        animal = Animal(
            name=name,
            species=species,
            habitat_id=habitat_id
        )
        await animal.save()
        return animal

    @staticmethod
    async def get_animals(in_habitat: Optional[bool] = None, 
                         needing_attention: Optional[bool] = None) -> List[Animal]:
        query = {}
        if in_habitat is not None:
            if in_habitat:
                query["habitat_id"] = {"$ne": None}
            else:
                query["habitat_id"] = None
                
        if needing_attention:
            query["status"] = {"$in": [AnimalStatus.SICK, AnimalStatus.INJURED]}
            
        return await Animal.find(query).to_list()