from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    phone: str
    address: Optional[str] = ""


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: Optional[str]
    is_admin: bool

    class Config:
        from_attributes = True


class RestaurantCreate(BaseModel):
    name: str
    description: str
    image: Optional[str] = ""
    delivery_time: str
    cuisine: str


class RestaurantOut(BaseModel):
    id: int
    name: str
    description: str
    image: Optional[str]
    rating: float
    delivery_time: str
    cuisine: str
    is_active: bool

    class Config:
        from_attributes = True


class MenuItemCreate(BaseModel):
    restaurant_id: int
    name: str
    description: str
    price: float
    image: Optional[str] = ""
    category: str


class MenuItemOut(BaseModel):
    id: int
    restaurant_id: int
    name: str
    description: str
    price: float
    image: Optional[str]
    category: str
    is_available: bool

    class Config:
        from_attributes = True


class OrderItemIn(BaseModel):
    menu_item_id: int
    quantity: int
    price: float


class OrderCreate(BaseModel):
    restaurant_id: int
    address: str
    items: List[OrderItemIn]
    total_amount: float


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    total_amount: float
    status: str
    address: str
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
