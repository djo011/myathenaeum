from attrs import asdict
from flask import redirect, render_template, request

from myathenaeum.db_models import Bookshelf
from myathenaeum import app, db

from myathenaeum.openlib import OpenLib


@app.route("/", methods=["POST", "GET"])
def index():
    ol = OpenLib()
    if request.method == "POST":
        isbn = request.form["content"]

        book = ol.get_full_book_info(isbn=isbn)

        new_book = Bookshelf(**asdict(book))

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect("/")
        except:
            return "There was an error adding new book"

    else:
        books = Bookshelf.query.order_by(Bookshelf.id).all()
        return render_template("index.html", books=books)


@app.route("/delete/<int:id>")
def delete(id):
    book_to_delete = Bookshelf.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return "There was a problem deleting the book"
