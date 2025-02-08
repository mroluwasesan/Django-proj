from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from books.models import books
from books.schemas import Book, BookUpdateModel
from typing import List



book_router = APIRouter()


@book_router.get("/", response_model=List[Book])
async def get_all_books():
    return books


@book_router.post("/",status_code=status.HTTP_201_CREATED,)
async def create_a_book(book_data: Book) -> dict:       
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book

@book_router.get("/{book_uid}")
async def get_book(book_uid: int) -> dict:
    for book in books:
        if book["id"] == book_uid:
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {book_uid} does not exist")

@book_router.patch("/{book_uid}", response_model=Book)
async def update_book(book_id: int, book_update_data: BookUpdateModel) -> dict:
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language
            return book
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {book_id} does not exist")

@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            book.remove(book)
        return {}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {book_id} does not exist")