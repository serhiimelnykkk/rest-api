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
    if books:
        max_id = max(book["id"] for book in books)
        new_id = max_id + 1
    else:
        new_id = 1
        
    book.id = new_id
        
    books.append(book)
    return book

@app.delete("/books/{book_id}", status_code=200)
async def delete_book(book_id: int):
    global books
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return {"message": "Book deleted"}
