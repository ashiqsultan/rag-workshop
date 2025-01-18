from typing import List
from pydantic import BaseModel


class Note(BaseModel):
    id: str
    title: str
    content: str
    created_at: str | None = None

class Notes(BaseModel):
    notes: List[Note]

class NotesCreate(BaseModel):
    title: str
    content: str
