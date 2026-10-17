# FastAPI Library API

A simple library management REST API built with FastAPI and Python.

## Features

- Retrieve all books
- Add a new book
- Retrieve a book by ID
- Update book information
- Delete a book
- Validate request data and handle missing books

## Technologies

- Python
- FastAPI
- Pydantic

## Installation

1. Clone this repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the application

```bash
fastapi dev main.py
```

## API Documentation

Once the server is running, open:

- API documentation: http://127.0.0.1:8000/docs
- Book list: http://127.0.0.1:8000/books

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/books` | Retrieve all books |
| POST | `/books` | Add a book |
| GET | `/books/{id}` | Retrieve a specific book |
| PATCH | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |

## Data Storage

Books are stored in an in-memory Python list. No database is used, so changes are not persistent after restarting the application.