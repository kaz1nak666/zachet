from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum

class BookStatus(str, Enum):
    READ = "прочитано"
    PLANNED = "в планах"

class BookBase(SQLModel):
    title: str
    author: str
    year: int
    status: BookStatus = BookStatus.PLANNED

class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    rating: Optional[int] = Field(default=None, ge=1, le=5)

class BookCreate(BookBase):
    pass

class BookUpdate(SQLModel):
    status: Optional[BookStatus] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)

class BookRead(BookBase):
    id: int
    rating: Optional[int] = None
