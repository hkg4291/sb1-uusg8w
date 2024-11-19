import pytest
from models.animal import Animal
from models.enums import AnimalStatus
from services.animal_service import AnimalService

@pytest.mark.asyncio
async def test_create_animal():
    animal_data = {
        "name": "Leo",
        "species": "Lion",
        "status": AnimalStatus.HEALTHY,
        "feeding_times": ["09:00", "17:00"],
        "dietary_requirements": {
            "food_type": "meat",
            "quantity_kg": 5
        }
    }
    
    animal = await AnimalService.create_animal(**animal_data)
    assert animal.name == "Leo"
    assert animal.species == "Lion"
    assert animal.status == AnimalStatus.HEALTHY

@pytest.mark.asyncio
async def test_get_animals_needing_attention():
    animals = await AnimalService.get_animals(needing_attention=True)
    assert all(a.status in [AnimalStatus.SICK, AnimalStatus.INJURED] 
              for a in animals)