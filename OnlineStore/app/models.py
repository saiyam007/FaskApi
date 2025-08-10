# SQLModel database models
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from pydantic import condecimal, constr, conint
from uuid import UUID, uuid4


class Product(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    sku: constr(min_length=1, max_length=50) = Field(unique=True, index=True, nullable=False)
    name: constr(min_length=1, max_length=100) = Field(nullable=False)
    price: condecimal(gt=0, max_digits=10, decimal_places=2) = Field(nullable=False)
    stock: conint(ge=0) = Field(default=0, nullable=False)
    
    

class Order(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    product_id: UUID = Field(nullable=False)
    quantity: conint(gt=0) = Field(nullable=False)
    status: constr(min_length=1, max_length=20) = Field(default="pending", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)    