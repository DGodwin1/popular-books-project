from flask import Flask, render_template, request

from .goodreads_data import(
    get_books_for_author,
    get_data_for_book_id,
    init as goodreads_init,
    )

app = Flask(__name__)

@app.before_first_request
def _app_init():
    goodreads_init()
    #needs to load key before

@app.route('/')
def homepage():
    #need to make authorname something that is requested from the user.
    #everything else stays the same.
    return render_template("main.html")

@app.route('/results',methods = ['POST', 'GET'])
def results():
    if request.method == 'POST':
        result = request.form
        author_name = result.get("author_name")
        books_for_author = get_books_for_author(author_name)
        first_book_id = books_for_author["books"][0]["book_id"]
        first_book = get_data_for_book_id(first_book_id)

    return render_template("results.html",first_book = first_book)

    #
    # return object with author + list of books.
