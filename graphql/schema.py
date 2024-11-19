import strawberry
from typing import List, Optional
from models.enums import AnimalStatus, EmployeeRole
from services.animal_service import AnimalService
from services.note_service import NoteService

@strawberry.type
class Animal:
    id: str
    name: str
    species: str
    status: AnimalStatus
    feeding_times: List[str]
    dietary_requirements: dict
    habitat_preferences: dict
    habitat_id: Optional[str]

@strawberry.type
class Note:
    id: str
    content: str
    employee_id: str
    animal_id: Optional[str]
    habitat_id: Optional[str]
    timestamp: str

@strawberry.type
class Query:
    @strawberry.field
    async def animals(
        self, 
        in_habitat: Optional[bool] = None, 
        needing_attention: Optional[bool] = None
    ) -> List[Animal]:
        return await AnimalService.get_animals(in_habitat, needing_attention)

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def createAnimal(
        self, 
        name: str, 
        species: str,
        habitat_id: Optional[str] = None
    ) -> Animal:
        return await AnimalService.create_animal(name, species, habitat_id)

    @strawberry.mutation
    async def createNote(
        self,
        content: str,
        employee_id: str,
        animal_id: Optional[str] = None,
        habitat_id: Optional[str] = None
    ) -> Note:
        return await NoteService.create_note(
            content, employee_id, animal_id, habitat_id
        )

schema = strawberry.Schema(query=Query, mutation=Mutation)