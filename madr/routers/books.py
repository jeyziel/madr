from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr.database import get_session
from madr.models import Book
from madr.schemas import BookListResponse, BookResponse, BookSchema, Message

router = APIRouter(prefix='/books', tags=['books'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=BookResponse)
def create_book(book: BookSchema, session: Session = Depends(get_session)):
    db_book = session.scalar(select(Book).where((Book.titulo == book.titulo)))

    if db_book:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=f'Book with name {db_book.titulo} already exists.',
        )

    book = Book(**book.model_dump())

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


@router.get('/', response_model=BookListResponse)
def read_books(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    books = session.scalars(select(Book).offset(skip).limit(limit)).all()

    return {'books': books}


@router.get('/{Book_id}', response_model=BookResponse)
def find_book(book_id: int, session: Session = Depends(get_session)):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Book with id {book_id} not found',
        )

    return db_book


@router.patch('/{book_id}', response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookSchema,
    session: Session = Depends(get_session),
):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Book with id {book_id} not found',
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)

    return db_book


@router.delete('/{book_id}', response_model=Message)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    db_book = session.scalar(select(Book).where(Book.id == book_id))

    if not db_book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Book with id {book_id} not found',
        )

    session.delete(db_book)
    session.commit()

    return {'message': 'Book has been deleted successfully.'}
