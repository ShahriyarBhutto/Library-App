from fastapi import FastAPI, HTTPException, status, Path, Query
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


class Library:
    book_id: int
    book_title: str
    book_author: str
    book_rating: int
    book_publish_year: int

    def __init__(self, book_id, book_title, book_author, book_rating, book_publish_year):
        self.book_id = book_id
        self.book_title = book_title
        self.book_author = book_author
        self.book_rating = book_rating
        self.book_publish_year = book_publish_year


class BookRequest(BaseModel):
    book_id: Optional[int] = Field(description="Id is not needed on creation",default=None)
    book_title: str = Field(min_length= 3)
    book_author: str = Field(min_length= 3)
    book_rating: int = Field(gt=0, lt=6)
    book_publish_year: int = Field(gt= 1900, lt= 2030)

    model_config = {
        "json_schema_extra":{
            "example":{
                "book_id":1,
                "book_title":"title-abc",
                "book_author":"author-abc",
                "book_rating":4,
                "book_publish_year":1995,


            }
        }
    }




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

@app.get("/books", status_code= status.HTTP_200_OK)
async def get_all_books():
    return LIBRARY

# Search Books By Their Id:

@app.get("/books/{book_id}" , status_code= status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in LIBRARY:
        if book.book_id == book_id:
            return book
    raise HTTPException(status_code= 404, detail="Item not found")

# Sort Books According to Publish Year

@app.get("/books/", status_code= status.HTTP_200_OK)
async def sort_books_by_year(book_year: int = Query(gt= 1900, lt= 2030)):
    books_to_return = []
    for book in LIBRARY:
        if book.book_publish_year == book_year:
            books_to_return.append(book)
    return books_to_return    


# Add New Books in the Library:

@app.post("/books/create_book", status_code = status.HTTP_201_CREATED )
async def add_new_book(request_book: BookRequest):
    new_book = Library(**request_book.model_dump())
    LIBRARY.append(find_the_id(new_book))



def find_the_id(book : Library):
    book.book_id = 1 if len(LIBRARY) == 0 else LIBRARY[-1].book_id + 1
    return book


# Updateing the Books:

@app.put("/books/update_book", status_code = status.HTTP_204_NO_CONTENT)
async def update_a_book(updated_book: BookRequest):
    book_changed = False
    for i in range(len(LIBRARY)):
        if LIBRARY[i].book_id == updated_book.book_id:
            LIBRARY[i] = updated_book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code= 404, detail="Item Not Fouud")

        
@app.delete("/books/{book_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_a_book(book_id: int = Path(gt=0)):
    book_changed = False
    for book in LIBRARY:
        if book.book_id == book_id:
            LIBRARY.remove(book)
            break
    if not book_changed:
        raise HTTPException(status_code= 404, detail="Item does not found")

        