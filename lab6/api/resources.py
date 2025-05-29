from flask import request, current_app
from flask_restful import Resource 
from marshmallow import ValidationError
from .models import db, Book
from .schemas import book_schema, books_schema


class BookListResource(Resource):
    def get(self):
        """
        Get a list of all books.
        ---
        tags:
          - Books
        parameters:
          - name: limit
            in: query
            type: integer
            required: false
            default: 10
            description: Number of books to return.
          - name: offset
            in: query
            type: integer
            required: false
            default: 0
            description: Number of books to skip.
        responses:
          200:
            description: A list of books.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    total:
                      type: integer
                    books:
                      type: array
                      items:
                        $ref: '#/components/schemas/Book'
        """
        limit = request.args.get('limit', current_app.config.get('ITEMS_PER_PAGE', 10), type=int)
        offset = request.args.get('offset', 0, type=int)

        books_query = Book.query.offset(offset).limit(limit).all()
        total_books = Book.query.count()

        return {
            "total": total_books,
            "books": books_schema.dump(books_query)
        }, 200

    def post(self):
        """
        Create a new book.
        ---
        tags:
          - Books
        requestBody:
          required: true
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/BookInput'
        responses:
          201:
            description: Book created successfully.
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Book'
          400:
            description: Invalid input data.
        """
        json_data = request.get_json()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        try:
            data = book_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 400

        if Book.query.filter_by(title=data['title'], author=data['author']).first():
             return {'message': 'Book with this title and author already exists'}, 400

        book = Book(title=data['title'], author=data['author'], year=data['year'])
        db.session.add(book)
        db.session.commit()
        return book_schema.dump(book), 201

class BookResource(Resource):
    def get(self, book_id):
        """
        Get a specific book by its ID.
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: The ID of the book to retrieve.
        responses:
          200:
            description: Details of the book.
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/Book'
          404:
            description: Book not found.
        """
        book = Book.query.get_or_404(book_id, description=f"Book with ID {book_id} not found")
        return book_schema.dump(book), 200

    def delete(self, book_id):
        """
        Delete a book by its ID.
        ---
        tags:
          - Books
        parameters:
          - name: book_id
            in: path
            type: integer
            required: true
            description: The ID of the book to delete.
        responses:
          200:
            description: Book deleted successfully.
          404:
            description: Book not found.
        """
        book = Book.query.get_or_404(book_id, description=f"Book with ID {book_id} not found")
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}, 200

def initialize_routes(current_api_instance):
    current_api_instance.add_resource(BookListResource, '/books')
    current_api_instance.add_resource(BookResource, '/books/<int:book_id>')