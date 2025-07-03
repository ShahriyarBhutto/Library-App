from fastapi import FastAPI



app = FastAPI()


class Library:
    book_id: int
    book_tilte: str
    book_author: str
    book_rating: int
    book_publish_year: int

    def __init__(self, book_id, book_title, book_author, book_rating, book_publish_year):
        self.book_id = book_id
        self.book_tilte = book_title
        self.book_author = book_author
        self.book_rating = book_rating
        self.book_publish_year = book_publish_year


LIBRARY = [
    Library(1,"Title-1","Author-1",5, 2010),
    Library(2,"Title-2","Author-2",5, 2010),
    Library(3,"Title-3","Author-3",4, 2012),
    Library(4,"Title-4","Author-4",5, 2011),
    Library(5,"Title-5","Author-5",2, 2012),
    Library(6,"Title-6","Author-6",1, 2010),
]


# Welcome Page:

@app.get("/")
async def home():
    return {"message":"Wellcome To Alpha Library"}

# Show All Books:

@app.get("/books")
async def get_all_books():
    return LIBRARY

# Search Books By Their Id:

@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    for book in LIBRARY:
        if book.book_id == book_id:
            return book

# Sort Books According to Publish Year

@app.get("/books/")
async def sort_books_by_year(book_year: int):
    books_to_return = []
    for book in LIBRARY:
        if book.book_publish_year == book_year:
            books_to_return.append(book)
    return books_to_return    