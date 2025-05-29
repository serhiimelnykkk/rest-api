from .extensions import db 

class Book(db.Model):
    __tablename__ = 'books_lab6' 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

    def to_dict(self): 
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }