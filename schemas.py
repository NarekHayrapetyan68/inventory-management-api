import enum
from pydantic import BaseModel
from typing import List, Optional


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    sent = "sent"
    delivered = "delivered"


class OrderBase(BaseModel):
    status: Optional[OrderStatusEnum] = OrderStatusEnum.pending


class OrderCreate(BaseModel):
    items: List[OrderItemBase]


class Order(OrderBase):
    id: int
    items: List[OrderItem]
    created_at: str

    class Config:
        orm_mode = True
