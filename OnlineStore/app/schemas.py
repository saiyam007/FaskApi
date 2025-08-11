# Pydantic request/response schemas
from typing import Optional
from pydantic import BaseModel, condecimal, conint, constr
from uuid import UUID
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"


# ---------- Product Schemas ----------
class ProductCreate(BaseModel):
    sku: constr(min_length=1, max_length=50)
    name: constr(min_length=1, max_length=100)
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    stock: conint(ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "sku": "SKU-1001",
                "name": "Wireless Mouse",
                "price": 19.99,
                "stock": 50
            }
        }


class ProductRead(ProductCreate):
    id: UUID


class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "price": 17.99,
                "stock": 45
            }
        }


# ---------- Order Schemas ----------
class OrderCreate(BaseModel):
    product_id: UUID
    quantity: conint(gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "11111111-1111-1111-1111-111111111111",
                "quantity": 2
            }
        }


class OrderRead(BaseModel):
    id: UUID
    product_id: UUID
    quantity: int
    status: OrderStatus
    created_at: datetime


class OrderUpdate(BaseModel):
    quantity: Optional[int] = None
    status: Optional[OrderStatus] = None

    class Config:
        json_schema_extra = {
            "example": {
                "status": "PAID"
            }
        }
