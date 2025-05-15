from flask import Blueprint, jsonify, request, abort, current_app
from .models import db, Book
from .schemas import book_schema, books_schema
from marshmallow import ValidationError

main_bp = Blueprint('main', __name__)

@main_bp.route("/books", methods=["GET"])
def get_books():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config['ITEMS_PER_PAGE'], type=int)
    offset = (page - 1) * limit

    books_query = Book.query.offset(offset).limit(limit).all()
    total_books = Book.query.count()

    return jsonify({
        "data": books_schema.dump(books_query),
        "total": total_books,
        "page": page,
        "limit": limit,
        "pages": (total_books + limit - 1) // limit 
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