
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None

books = [
    {"id": 1, "title": "Python Basics", "author": "Ali"},
    {"id": 2, "title": "Learning FastAPI", "author": "Sara"}
]


@app.get("/books")
def get_books():
    return books


class Book(BaseModel):
    title: str
    author: str

@app.post("/books")
def add_book(book: Book):
    new_book = {
        "id": max((book["id"] for book in books), default=0) + 1,
        "title": book.title,
        "author": book.author
    }

    books.append(new_book)
    return new_book



@app.get("/books/{id}")
def get_book(id: int):
    for book in books:
        if book["id"] == id:
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )


@app.patch("/books/{id}")
def update_book(id: int, book_update: BookUpdate):
    if not book_update.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided"
        )
    for book in books:
        if book["id"] == id:
            update_data = book_update.model_dump(exclude_unset=True)
            book.update(update_data)
            return book

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )

@app.delete("/books/{id}")
def delete_book(id: int):
    for index, book in enumerate(books):
        if book["id"] == id:
            deleted_book = books.pop(index)
            return {
                "message": "Book deleted successfully",
                "book": deleted_book
            }

    raise HTTPException(
        status_code=404,
        detail="Book not found"
    )
