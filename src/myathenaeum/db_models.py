from myathenaeum import db


class Bookshelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    publisher = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return super().__repr__()
