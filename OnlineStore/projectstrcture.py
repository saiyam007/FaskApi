import os

# Define folder structure
folders = [
    "OnlineStore/app/api",
    "OnlineStore/tests"
]

files = {
    "OnlineStore/app/__init__.py": "",
    "OnlineStore/app/main.py": "# FastAPI app entrypoint\nfrom fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\nasync def root():\n    return {\"message\": \"Hello World\"}\n",
    "OnlineStore/app/config.py": "# Configuration settings\n",
    "OnlineStore/app/models.py": "# SQLModel database models\n",
    "OnlineStore/app/schemas.py": "# Pydantic request/response schemas\n",
    "OnlineStore/app/crud.py": "# CRUD operations\n",
    "OnlineStore/app/database.py": "# Database engine and session setup\n",
    "OnlineStore/app/deps.py": "# Dependency functions\n",
    "OnlineStore/app/api/__init__.py": "",
    "OnlineStore/app/api/routes.py": "# API routes\n",
    "OnlineStore/app/api/webhooks.py": "# webhooks routes\n",
    "OnlineStore/tests/__init__.py": "",
    "OnlineStore/tests/test_crud.py": "# Unit tests for CRUD\n",
    "OnlineStore/tests/test_routes.py": "# API endpoint tests\n",
    "OnlineStore/tests/conftest.py": "# Pytest fixtures\n",
    "OnlineStore/requirements.txt": "fastapi==0.111.0\nuvicorn[standard]==0.30.1\nsqlmodel==0.0.16\nrequests==2.32.3\npytest==8.2.2\npytest-asyncio==0.23.8\n",
    "OnlineStore/.env": "# Environment variables\n",
    "OnlineStore/.gitignore": "*.pyc\n__pycache__/\n.env\n",
    "OnlineStore/README.md": "# FastAPI CRUD Service\n"
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Project structure created successfully!")
