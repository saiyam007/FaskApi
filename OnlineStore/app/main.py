# FastAPI app entrypoint
from fastapi import FastAPI
from .api import routes, webhooks  # Import your API routes if they exist
from .database import init_db  # Uncomment if you have init_db()

app = FastAPI(
    title="Online Store API",
    version="1.0.0",
    description="""
    A FastAPI service for managing Products and Orders with secure Payment Webhooks.

    Features:
    - Create, list, update, and delete products
    - Create orders with stock checks
    - Update or cancel orders with state validation
    """,
)

# Include routes with tags defined in routes.py
# Normal CRUD routes
app.include_router(routes.router)

# Webhook routes
app.include_router(webhooks.router) 

@app.get('/', tags=["Health"])
async def root():
    """
    Root endpoint for health check.
    """
    return {"message": "Welcome to the Online Store API"}

# If you want to initialize the DB at startup
@app.on_event("startup")
def on_startup():
    init_db()
