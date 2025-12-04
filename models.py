from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Note:
    id: str
    text: str
    date: str

@dataclass
class Book:
    id: str
    title: str
    author: str
    genre: str
    year: int
    status: str
    date_added: str
    date_finished: Optional[str] = None
    notes: List[Note] = field(default_factory=list)
    cover_image: Optional[str] = None
