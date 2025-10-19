from myathenaeum import db

class Bookshelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return super().__repr__()