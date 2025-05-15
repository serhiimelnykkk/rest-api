from flask import Flask, jsonify, request, abort
from .models import books
from .schemas import BookSchema
from marshmallow import ValidationError

app = Flask(__name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books_schema.dump(books))

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        abort(404, description="Book not found")
    return jsonify(book_schema.dump(book))

@app.route("/books", methods=["POST"])
def add_book():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    if books:
        max_id = max(book["id"] for book in books)
        new_id = max_id + 1
    else:
        new_id = 1
    
    book_data["id"] = new_id

    books.append(book_data)
    return jsonify(book_schema.dump(book_data)), 201

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        abort(404, description="Book not found")
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"}), 200
