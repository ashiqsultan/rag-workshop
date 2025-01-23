from typing import List, Optional
from pydantic import BaseModel


class Note(BaseModel):
    id: str
    title: str
    content: str
    created_at: Optional[str] = None


class Notes(BaseModel):
    notes: List[Note]


class NotesCreate(BaseModel):
    title: str
    content: str
