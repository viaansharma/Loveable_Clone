# Simple Blog API

A minimal **RESTful** blog API built with **FastAPI**, **SQLite**, and **SQLAlchemy**. It demonstrates a clean project layout, basic CRUD operations, and easy setup for developers who want a quick start with modern Python web development.

---

## Tech Stack

| Component | Version | Description |
|-----------|---------|-------------|
| **FastAPI** | `0.110.0` | High‑performance web framework for building APIs with Python 3.7+ based on standard Python type hints. |
| **Uvicorn** | `0.27.0` | Lightning‑fast ASGI server used to run the FastAPI app. |
| **SQLite** | Built‑in | Server‑less, self‑contained, zero‑configuration SQL database engine – perfect for small projects and demos. |
| **SQLAlchemy** | `2.0.23` | Powerful ORM that abstracts away raw SQL while still allowing fine‑grained control. |
| **Pydantic** | `2.5.2` | Data validation and settings management using Python type annotations. |
| **python-dotenv** | `1.0.0` | Loads environment variables from a `.env` file for easy configuration. |

---

## Project Structure

```
simple_blog_api/
│
├─ app/
│   ├─ __init__.py          # Makes `app` a package
│   ├─ main.py              # FastAPI application instance & router inclusion
│   ├─ models.py            # SQLAlchemy models (Post, User, etc.)
│   ├─ schemas.py           # Pydantic models for request/response bodies
│   ├─ crud.py              # Database‑access helper functions
│   └─ database.py          # Engine, SessionLocal, Base declarative
│
├─ .env                     # Environment variables (e.g., DATABASE_URL)
├─ requirements.txt         # Python dependencies
└─ README.md                # This documentation
```

- **`app/main.py`** – Creates the FastAPI instance, includes the API router, and starts the application.
- **`app/models.py`** – Defines the SQLAlchemy ORM models that map to SQLite tables.
- **`app/schemas.py`** – Pydantic models that shape the request payloads and response schemas.
- **`app/crud.py`** – Encapsulates all database operations (create, read, update, delete) to keep the route handlers clean.
- **`app/database.py`** – Sets up the SQLite engine, session maker, and Base class for model definitions.
- **`.env`** – Stores configuration like `DATABASE_URL=sqlite:///./blog.db`. The file is ignored by version control.

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your‑username/simple_blog_api.git
cd simple_blog_api
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Configure environment variables
Create a `.env` file in the project root:
```dotenv
# .env
DATABASE_URL=sqlite:///./blog.db
```
If you omit this file, the default SQLite database (`blog.db` in the project root) will be used.

### 5. Run the API
```bash
uvicorn app.main:app --reload
```
- `--reload` enables hot‑reloading during development.
- The API will be available at `http://127.0.0.1:8000`.

### 6. Interactive docs
FastAPI automatically generates Swagger UI and ReDoc documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## API Endpoints

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| **GET** | `/posts/` | Retrieve a list of all blog posts. | – | `[{id, title, content, created_at, updated_at}]` |
| **GET** | `/posts/{post_id}` | Retrieve a single post by its ID. | – | `{id, title, content, created_at, updated_at}` |
| **POST** | `/posts/` | Create a new blog post. | `{title, content}` | `{id, title, content, created_at, updated_at}` |
| **PUT** | `/posts/{post_id}` | Fully update an existing post. | `{title, content}` | `{id, title, content, created_at, updated_at}` |
| **PATCH** | `/posts/{post_id}` | Partially update a post (e.g., only title). | `{title?, content?}` | `{id, title, content, created_at, updated_at}` |
| **DELETE** | `/posts/{post_id}` | Delete a post permanently. | – | `{detail: "Post deleted"}` |

> **Note**: The actual implementation may also include user authentication routes (`/users/`, `/auth/`) – they follow the same CRUD pattern.

---

## Example `curl` Requests

### Create a post
```bash
curl -X POST "http://127.0.0.1:8000/posts/" \
     -H "Content-Type: application/json" \
     -d '{"title": "My First Post", "content": "Hello, FastAPI!"}'
```

### Get all posts
```bash
curl http://127.0.0.1:8000/posts/
```

### Get a single post (ID = 1)
```bash
curl http://127.0.0.1:8000/posts/1
```

### Update a post completely (ID = 1)
```bash
curl -X PUT "http://127.0.0.1:8000/posts/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Title", "content": "Updated content."}'
```

### Partially update a post (only title)
```bash
curl -X PATCH "http://127.0.0.1:8000/posts/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "Title Only Update"}'
```

### Delete a post (ID = 1)
```bash
curl -X DELETE "http://127.0.0.1:8000/posts/1"
```

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests. When adding new features, keep the following in mind:
- Follow the existing project layout.
- Write Pydantic schemas for any new request/response models.
- Add unit tests under a `tests/` directory (if the project grows).
- Update this README with any new endpoints or setup steps.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.
