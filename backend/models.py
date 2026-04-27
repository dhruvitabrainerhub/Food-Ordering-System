from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone = Column(String)
    address = Column(Text)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    orders = relationship("Order", back_populates="user")


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    image = Column(String)
    rating = Column(Float, default=0.0)
    delivery_time = Column(String)
    cuisine = Column(String)
    is_active = Column(Boolean, default=True)
    items = relationship("MenuItem", back_populates="restaurant")


class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    name = Column(String)
    description = Column(Text)
    price = Column(Float)
    image = Column(String)
    category = Column(String)
    is_available = Column(Boolean, default=True)
    restaurant = relationship("Restaurant", back_populates="items")


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    total_amount = Column(Float)
    status = Column(
        String, default="pending"
    )  # pending, confirmed, preparing, delivered, cancelled
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer)
    price = Column(Float)
    order = relationship("Order", back_populates="items")
