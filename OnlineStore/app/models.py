from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import condecimal, constr, conint
from uuid import UUID, uuid4
from enum import Enum


# Allowed order statuses
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"


# Product model
class Product(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    sku: constr(min_length=1, max_length=50) = Field(unique=True, index=True, nullable=False)
    name: constr(min_length=1, max_length=100) = Field(nullable=False)
    price: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(nullable=False)
    stock: conint(ge=0) = Field(default=0, nullable=False)


# Order model
class Order(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(nullable=False)  # product reference
    quantity: conint(gt=0) = Field(nullable=False)
    status: OrderStatus = Field(default=OrderStatus.PENDING, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)