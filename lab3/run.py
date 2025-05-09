from api import create_app, db
from api.models import Book 

app = create_app()

def create_tables_and_seed_data():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

        if Book.query.count() == 0:
            initial_books = [
                {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
                {"id": 2, "title": "1984", "author": "George Orwell", "year": 1949},
                {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
                {"id": 4, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "year": 1951},
                {"id": 5, "title": "Pride and Prejudice", "author": "Jane Austen", "year": 1813},
            ]
            for book_data in initial_books:
                if not Book.query.get(book_data["id"]):
                    book = Book(id=book_data["id"], title=book_data["title"], author=book_data["author"], year=book_data["year"])
                    db.session.add(book)
            db.session.commit()
            print("Initial data seeded.")
        else:
            print("Database already seeded or contains data.")


if __name__ == "__main__":
    create_tables_and_seed_data()
    app.run(debug=True, host='0.0.0.0')