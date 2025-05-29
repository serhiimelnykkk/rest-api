from fastapi import FastAPI, HTTPException, Body, status
from typing import List
from .db import connect_to_mongo, close_mongo_connection, get_database
from .models import BookCreate, BookDB
from bson import ObjectId 

app = FastAPI(title="Library API with FastAPI and MongoDB")

BOOKS_COLLECTION = "books" 

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.post("/books", response_model=BookDB, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate = Body(...)):
    db = get_database()
    book_dict = book.model_dump()

    result = await db[BOOKS_COLLECTION].insert_one(book_dict)
    created_book = await db[BOOKS_COLLECTION].find_one({"_id": result.inserted_id})
    if created_book:
        return BookDB(**created_book) 
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create book")


@app.get("/books", response_model=List[BookDB])
async def get_all_books(limit: int = 10, skip: int = 0): 
    db = get_database()
    books_cursor = db[BOOKS_COLLECTION].find({}).skip(skip).limit(limit)
    books_list = []
    async for book_doc in books_cursor:
        books_list.append(BookDB(**book_doc))
    return books_list


@app.get("/books/{book_id_str}", response_model=BookDB)
async def get_book_by_id(book_id_str: str):
    db = get_database()
    try:
        book_oid = ObjectId(book_id_str)
    except Exception: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid book ID format: {book_id_str}")

    book = await db[BOOKS_COLLECTION].find_one({"_id": book_oid})
    if book:
        return BookDB(**book)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id_str} not found")


@app.delete("/books/{book_id_str}", status_code=status.HTTP_200_OK)
async def delete_book_by_id(book_id_str: str):
    db = get_database()
    try:
        book_oid = ObjectId(book_id_str)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid book ID format: {book_id_str}")

    result = await db[BOOKS_COLLECTION].delete_one({"_id": book_oid})

    if result.deleted_count == 1:
        return {"message": f"Book with id {book_id_str} deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {book_id_str} not found")