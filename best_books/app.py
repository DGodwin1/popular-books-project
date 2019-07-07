from flask import Flask, render_template

from .goodreads_data import get_books_for_author
from .goodreads_data import init as goodreads_init

app = Flask(__name__)

@app.before_first_request
def _app_init():
    goodreads_init()
    #needs to load key before

@app.route('/')
def homepage():
    author_name = "Thomas Pynchon"
    books_for_author = get_books_for_author(author_name)
    first_book = books_for_author["books"][0]

#return object with author + list of books.
    return render_template("main.html",author_name = author_name, first_book = first_book )
