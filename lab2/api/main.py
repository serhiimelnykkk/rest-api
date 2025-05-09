from fastapi import FastAPI, HTTPException
from typing import List
from .models import books
from .schemas import Book

app = FastAPI()

@app.get("/books", response_model=List[Book])
async def get_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books", response_model=Book, status_code=201)
async def add_book(book: Book):
    if any(b["id"] == book.id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists.")
    books.append(book.dict())
    return book

@app.delete("/books/{book_id}", status_code=200)
async def delete_book(book_id: int):
    global books
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return {"message": "Book deleted"}
