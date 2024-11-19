from fastapi import APIRouter, HTTPException, Request, Response
from typing import List, Optional
from models.animal import Animal
from models.habitat import Habitat
from models.note import Note
from services.cache import cache_response
from config import settings

router = APIRouter(tags=["zoo"])

@router.get("/animals", response_model=List[dict])
@cache_response()
async def list_animals(
    request: Request,
    response: Response,
    species: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = settings.PAGE_SIZE
):
    query = {}
    if species:
        query["species"] = species
    if status:
        query["status"] = status
    
    animals = await Animal.find(query).skip(skip).limit(limit).to_list()
    if not animals:
        return []
    return [animal.dict() for animal in animals]

@router.get("/animals/{animal_id}", response_model=dict)
@cache_response()
async def get_animal(animal_id: str, request: Request):
    animal = await Animal.get(animal_id)
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal.dict()

@router.get("/habitats/{habitat_id}/animals", response_model=List[dict])
@cache_response()
async def get_habitat_animals(
    habitat_id: str,
    request: Request,
    skip: int = 0,
    limit: int = settings.PAGE_SIZE
):
    animals = await Animal.find(
        {"habitat_id": habitat_id}
    ).skip(skip).limit(limit).to_list()
    if not animals:
        return []
    return [animal.dict() for animal in animals]

@router.get("/animals/{animal_id}/notes", response_model=List[dict])
@cache_response()
async def get_animal_notes(
    animal_id: str,
    request: Request,
    skip: int = 0,
    limit: int = settings.PAGE_SIZE
):
    notes = await Note.find(
        {"animal_id": animal_id}
    ).sort(-Note.timestamp).skip(skip).limit(limit).to_list()
    if not notes:
        return []
    return [note.dict() for note in notes]

@router.get("/habitats/summary", response_model=List[dict])
@cache_response(timeout=3600)  # Cache for 1 hour
async def get_habitats_summary(request: Request):
    habitats = await Habitat.find_all().to_list()
    if not habitats:
        return []
        
    summary = []
    for habitat in habitats:
        animal_count = await Animal.find({"habitat_id": str(habitat.id)}).count()
        summary.append({
            "id": str(habitat.id),
            "name": habitat.name,
            "type": habitat.type,
            "capacity": habitat.capacity,
            "current_occupancy": animal_count,
            "available_space": habitat.capacity - animal_count
        })
    
    return summary