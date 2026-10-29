import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from psycopg.rows import dict_row

load_dotenv()

app = FastAPI()


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"host={DB_HOST} "
    f"port={DB_PORT} "
    f"dbname={DB_NAME} "
    f"user={DB_USER} "
    f"password={DB_PASSWORD}"
)


class Book(BaseModel):
    title: str
    author: str


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None


def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


@app.get("/books")
def get_books():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, author FROM books ORDER BY id")
            return cur.fetchall()


@app.post("/books")
def add_book(book: Book):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO books (title, author)
                VALUES (%s, %s)
                RETURNING id, title, author
                """,
                (book.title, book.author),
            )
            return cur.fetchone()


@app.get("/books/{id}")
def get_book(id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, title, author FROM books WHERE id = %s",
                (id,),
            )
            book = cur.fetchone()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.patch("/books/{id}")
def update_book(id: int, book_update: BookUpdate):
    update_data = book_update.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided",
        )

    allowed_fields = {"title", "author"}
    fields = [field for field in update_data if field in allowed_fields]
    values = [update_data[field] for field in fields]

    set_clause = ", ".join(f"{field} = %s" for field in fields)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                UPDATE books
                SET {set_clause}
                WHERE id = %s
                RETURNING id, title, author
                """,
                (*values, id),
            )
            book = cur.fetchone()

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.delete("/books/{id}")
def delete_book(id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM books
                WHERE id = %s
                RETURNING id, title, author
                """,
                (id,),
            )
            deleted_book = cur.fetchone()

    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return {
        "message": "Book deleted successfully",
        "book": deleted_book,
    }
