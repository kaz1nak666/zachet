from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from db import get_session
from models import Book, BookCreate, BookUpdate, BookRead

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, session: Session = Depends(get_session)):
    db_book = Book.model_validate(book_in)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookRead])
def read_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()
    return books

@router.patch("/{id}", response_model=BookRead)
def update_book(id: int, book_in: BookUpdate, session: Session = Depends(get_session)):
    db_book = session.get(Book, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    
    book_data = book_in.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id: int, session: Session = Depends(get_session)):
    db_book = session.get(Book, id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    session.delete(db_book)
    session.commit()
    return None
