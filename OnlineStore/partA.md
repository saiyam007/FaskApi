# Part A Environment & Project Setup

# # Questions
# Q1. What Python version and minimal dependencies will you choose for a FastAPI CRUD  service? Justify each package.

# Ans : Python Version Python 3.12.x

1.Fully supported by FastAPI and SQLAlchemy/SQLModel as of mid-2024.
2.Brings better performance in function calls and comprehensions compared to 3.11.
3.Has longer support window for future-proofing.
4.Still safe for production use — no major ecosystem breakages. 

| Package                        | Purpose          | Why This Package                                                                                 |
| ------------------------------ | ---------------- | ------------------------------------------------------------------------------------------------ |
| **fastapi==0.111.0**           | Web framework    | High-performance, async-ready, built-in validation using Pydantic v2.                            |
| **uvicorn\[standard]==0.30.1** | ASGI server      | Runs your FastAPI app with fast networking stack (`uvloop`, `httptools`) for better performance. |
| **sqlmodel==0.0.16**           | ORM + validation | Combines SQLAlchemy (ORM) and Pydantic (data validation) — clean and concise CRUD.               |
| **requests==2.32.3**           | HTTP client      | Used in black-box API endpoint tests.                                                            |
| **pytest==8.2.2**              | Test runner      | Industry standard testing framework.                                                             |
| **pytest-asyncio==0.23.8**     | Async tests      | Lets you test `async` CRUD operations cleanly.                                                   |


# Q2. How will you structure folders so that your code is readable and testable (e.g., app/, tests/)? Provide the final tree.

# Ans :
**Final Tree**
```
project_root/
├── app/                      # Main application package
│   ├── __init__.py           # Marks this as a Python package
│   ├── main.py               # Entry point of FastAPI app (creates app instance, mounts routes)
│   ├── config.py             # Configurations like DB URL, API settings, env vars
│   ├── models.py             # SQLModel models that define database tables
│   ├── schemas.py            # Pydantic models for request/response payloads
│   ├── crud.py               # Database operations (Create, Read, Update, Delete)
│   ├── database.py           # SQLAlchemy/SQLModel database engine + session setup
│   ├── deps.py               # Dependency injection helpers (e.g., `get_db`)
│   └── api/                  # Folder for API routes
│       ├── __init__.py
│       └── routes.py         # All CRUD route definitions (GET, POST, PUT, DELETE)
│
├── tests/                    # Automated tests
│   ├── __init__.py
│   ├── test_crud.py          # Unit tests for CRUD logic (functions in crud.py)
│   ├── test_routes.py        # API endpoint tests
│   └── conftest.py           # Pytest fixtures (test DB, FastAPI client)
│
├── requirements.txt          # List of pinned Python dependencies
├── .env                      # Environment variables (optional, e.g., DB URL)
├── .gitignore                # Files/folders to ignore in Git
└── README.md                 # Documentation for your project

```

**Why This Layout Works for the Challenge**
- Keeps **logic separate** from **routes** for easy testing.
- API folder allows for **versioning** (e.g., `api/v1`) later.
- **`schemas.py`** prevents direct DB model exposure.
- Mirrors structure in `tests/` so navigation is easy.
- Works whether you use **SQLite in-memory** or a persistent DB.

**requirements.txt** (pinned versions)
```txt
fastapi==0.111.0
uvicorn[standard]==0.30.1
sqlmodel==0.0.16
requests==2.32.3
pytest==8.2.2
pytest-asyncio==0.23.8
```
