from typing import List
from pydantic import BaseModel


class Note(BaseModel):
    id: str
    content: str

class Notes(BaseModel):
    notes: List[Note]

class NotesCreate(BaseModel):
    note: str
