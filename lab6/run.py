from api import create_app, db
from api.models import Book 

app = create_app()

def create_tables_and_seed_data():
    with app.app_context():
        db.create_all()
        print("Database tables created (if not exist). Table name: books_lab6")

        if Book.query.count() == 0:
            initial_books = [
                {"title": "Flask-RESTful Guide", "author": "Mr. Flask", "year": 2023},
                {"title": "SQLAlchemy Deep Dive", "author": "Database Guru", "year": 2022},
            ]
            for book_data in initial_books:
                if not Book.query.filter_by(title=book_data["title"], author=book_data["author"]).first():
                    book = Book(title=book_data["title"], author=book_data["author"], year=book_data["year"])
                    db.session.add(book)
            db.session.commit()
            print("Initial data seeded for Lab 6.")
        else:
            print("Database for Lab 6 already seeded or contains data.")


if __name__ == "__main__":
    create_tables_and_seed_data()
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule, "Methods:", rule.methods, "Endpoint:", rule.endpoint)
    app.run(debug=True, host='0.0.0.0', port=5002)