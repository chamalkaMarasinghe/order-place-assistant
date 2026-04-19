from pydantic import BaseModel, Field
from typing import List

class RetrievalPlan(BaseModel):
    strategy: str
    value: str
    pages: int = Field(ge=1, le=5)

class Product(BaseModel):
    id: int
    title: str
    price: float

class OrderItem(BaseModel):
    id: int
    title: str
    price: float
    quantity: int = Field(ge=1)