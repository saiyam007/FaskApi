# CRUD operations
from sqlmodel import Session, select
from fastapi import HTTPException, status
from uuid import UUID
from . import models, schemas

# ---------- Product CRUD ----------
def create_product(session: Session, product_in: schemas.ProductCreate):
    existing = session.exec(select(models.Product).where(models.Product.sku == product_in.sku)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="SKU already exists")
    product = models.Product(**product_in.dict())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_products(session: Session):
    return session.exec(select(models.Product)).all()

def get_product(session: Session, product_id: UUID):
    product = session.get(models.Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

def update_product(session: Session, product_id: UUID, product_in: schemas.ProductUpdate):
    product = get_product(session, product_id)
    for key, value in product_in.dict(exclude_unset=True).items():
        setattr(product, key, value)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def delete_product(session: Session, product_id: UUID):
    product = get_product(session, product_id)
    session.delete(product)
    session.commit()

# ---------- Order CRUD ----------
def create_order(session: Session, order_in: schemas.OrderCreate):
    product = session.get(models.Product, order_in.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.stock < order_in.quantity:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Insufficient stock")
    product.stock -= order_in.quantity
    order = models.Order(product_id=order_in.product_id, quantity=order_in.quantity)
    session.add(order)
    session.add(product)
    session.commit()
    session.refresh(order)
    return order

def get_order(session: Session, order_id: UUID):
    order = session.get(models.Order, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

def update_order(session: Session, order_id: UUID, order_in: schemas.OrderUpdate):
    order = get_order(session, order_id)
    if order_in.status:
        if order.status == schemas.OrderStatus.SHIPPED and order_in.status == schemas.OrderStatus.PENDING:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state transition")
        order.status = order_in.status
    if order_in.quantity:
        product = session.get(models.Product, order.product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        if product.stock + order.quantity < order_in.quantity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Insufficient stock")
        product.stock += order.quantity - order_in.quantity
        order.quantity = order_in.quantity
        session.add(product)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def delete_order(session: Session, order_id: UUID):
    order = get_order(session, order_id)
    if order.status != schemas.OrderStatus.PENDING:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete non-pending orders")
    session.delete(order)
    session.commit()
