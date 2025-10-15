from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from openlib import OpenLib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///athenaeum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Avoids a warning
db = SQLAlchemy(app)


class Bookshelf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    author = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return super().__repr__()


@app.route('/', methods=['POST', 'GET'])
def index():
    ol = OpenLib()
    if request.method == 'POST':
        isbn = request.form['content']
        book_content = ol.get_book(isbn)
        author_key = book_content.authors[0]["key"]
        author_content = ol.get_author(author_key=author_key)
        
        new_book = Bookshelf(id = isbn, title = book_content.title, author=author_content.name)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error adding new book'
    
    else:
        books = Bookshelf.query.order_by(Bookshelf.id).all()
        return render_template('index.html', books=books)
    

    return render_template('index.html')

@app.route('/delete/<int:id>')
def delete(id):
    book_to_delete = Bookshelf.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting the book"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)