from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import desc, asc 
from .models import db, Book
from .schemas import book_schema, books_schema 
from marshmallow import ValidationError 

main_bp = Blueprint('main', __name__)

def get_next_page_url(last_book_id, limit, base_url="/books"):
    if last_book_id is None:
        return None
    return f"{base_url}?cursor={last_book_id}&limit={limit}"

@main_bp.route("/books", methods=["GET"])
def get_books():
    cursor = request.args.get('cursor', type=int)
    limit = request.args.get('limit', current_app.config.get('ITEMS_PER_PAGE', 10), type=int)

    query = Book.query.order_by(Book.id.asc())

    if cursor:
        query = query.filter(Book.id > cursor)

    books_page = query.limit(limit).all()

    next_cursor = None
    if books_page and len(books_page) == limit:
        next_cursor = books_page[-1].id

    next_page_link = None
    if next_cursor:
        next_page_link = get_next_page_url(next_cursor, limit, request.base_url)


    return jsonify({
        "data": books_schema.dump(books_page),
        "pagination": {
            "next_cursor": next_cursor,
            "next_page_url": next_page_link,
            "limit": limit
        }
    })

@main_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get_or_404(book_id, description="Book not found")
    return jsonify(book_schema.dump(book))

@main_bp.route("/books", methods=["POST"])
def add_book():
    try:
        if not request.is_json:
            return jsonify({"error": "Missing JSON in request"}), 400
        book_data = book_schema.load(request.json) 
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": "Internal server error during request processing"}), 500

    max_id = db.session.query(db.func.max(Book.id)).scalar()

    if max_id:
        new_id = max_id + 1
    else:
        new_id = 1

    new_book = Book(
        id=new_id,
        title=book_data["title"],
        author=book_data["author"],
        year=book_data["year"]
    )
    db.session.add(new_book)
    db.session.commit()

    return jsonify(book_schema.dump(new_book)), 201 

@main_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id, description="Book not found")
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200