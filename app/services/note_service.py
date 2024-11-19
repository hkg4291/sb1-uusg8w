from typing import Optional
from app.models.note import Note

class NoteService:
    @staticmethod
    async def create_note(
        content: str,
        employee_id: str,
        animal_id: Optional[str] = None,
        habitat_id: Optional[str] = None
    ) -> Note:
        note = Note(
            content=content,
            employee_id=employee_id,
            animal_id=animal_id,
            habitat_id=habitat_id
        )
        await note.save()
        return note