# API routes
# API routes
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from .. import crud, schemas, database

router = APIRouter()

# ---------- Products ----------
@router.post(
    "/products",
    response_model=schemas.ProductRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
    summary="Create a new product",
    description="Create a new product with a unique SKU, price greater than 0, and stock greater than or equal to 0."
)
def create_product(product_in: schemas.ProductCreate, session: Session = Depends(database.get_session)):
    return crud.create_product(session, product_in)


@router.get(
    "/products",
    response_model=list[schemas.ProductRead],
    tags=["Products"],
    summary="List all products",
    description="Retrieve all products. Pagination can be added later if dataset grows."
)
def list_products(session: Session = Depends(database.get_session)):
    return crud.get_products(session)


@router.get(
    "/products/{product_id}",
    response_model=schemas.ProductRead,
    tags=["Products"],
    summary="Get a product by ID",
    description="Retrieve a single product by its UUID. Returns 404 if the product does not exist."
)
def read_product(product_id: UUID, session: Session = Depends(database.get_session)):
    return crud.get_product(session, product_id)


@router.put(
    "/products/{product_id}",
    response_model=schemas.ProductRead,
    tags=["Products"],
    summary="Update a product",
    description="Update product details. Partial updates are supported by sending only the fields to change."
)
def update_product(product_id: UUID, product_in: schemas.ProductUpdate, session: Session = Depends(database.get_session)):
    return crud.update_product(session, product_id, product_in)


@router.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Products"],
    summary="Delete a product",
    description="Delete a product by its UUID. Returns 404 if the product does not exist."
)
def delete_product(product_id: UUID, session: Session = Depends(database.get_session)):
    crud.delete_product(session, product_id)
    return None


# ---------- Orders ----------
@router.post(
    "/orders",
    response_model=schemas.OrderRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Orders"],
    summary="Create a new order",
    description="Create an order for a product. Reduces stock atomically. Returns 409 if stock is insufficient."
)
def create_order(order_in: schemas.OrderCreate, session: Session = Depends(database.get_session)):
    return crud.create_order(session, order_in)

@router.get("/orders", response_model=list[schemas.OrderRead])
def list_orders(session: Session = Depends(database.get_session)):
    """Fetch all orders."""
    return crud.get_orders(session)

@router.get(
    "/orders/{order_id}",
    response_model=schemas.OrderRead,
    tags=["Orders"],
    summary="Get an order by ID",
    description="Retrieve order details including product ID, quantity, status, and creation timestamp."
)
def read_order(order_id: UUID, session: Session = Depends(database.get_session)):
    return crud.get_order(session, order_id)


@router.put(
    "/orders/{order_id}",
    response_model=schemas.OrderRead,
    tags=["Orders"],
    summary="Update an order",
    description="Update order quantity or status. Prevents invalid state transitions such as SHIPPED → PENDING."
)
def update_order(order_id: UUID, order_in: schemas.OrderUpdate, session: Session = Depends(database.get_session)):
    return crud.update_order(session, order_id, order_in)


@router.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Orders"],
    summary="Delete an order",
    description="Delete an order only if it is in PENDING status. Otherwise, change status to CANCELED."
)
def delete_order(order_id: UUID, session: Session = Depends(database.get_session)):
    crud.delete_order(session, order_id)
    return None


