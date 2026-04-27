from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from models import MenuItem, Order, Restaurant, User
from routers.auth import get_current_user
from schemas import MenuItemCreate, MenuItemOut, RestaurantCreate, RestaurantOut

router = APIRouter(prefix="/admin", tags=["admin"])
security = HTTPBearer()


def admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    user = get_current_user(credentials.credentials, db)
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# Dashboard stats
@router.get("/stats")
def get_stats(db: Session = Depends(get_db), user=Depends(admin_user)):
    return {
        "total_users": db.query(User).count(),
        "total_restaurants": db.query(Restaurant).count(),
        "total_orders": db.query(Order).count(),
        "pending_orders": db.query(Order).filter(Order.status == "pending").count(),
    }


# Restaurant CRUD
@router.post("/restaurants", response_model=RestaurantOut)
def add_restaurant(
    data: RestaurantCreate, db: Session = Depends(get_db), user=Depends(admin_user)
):
    r = Restaurant(**data.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.get("/restaurants", response_model=List[RestaurantOut])
def list_restaurants(db: Session = Depends(get_db), user=Depends(admin_user)):
    return db.query(Restaurant).all()


@router.put("/restaurants/{rid}/toggle")
def toggle_restaurant(
    rid: int, db: Session = Depends(get_db), user=Depends(admin_user)
):
    r = db.query(Restaurant).filter(Restaurant.id == rid).first()
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    r.is_active = not r.is_active
    db.commit()
    return {"is_active": r.is_active}


@router.delete("/restaurants/{rid}")
def delete_restaurant(
    rid: int, db: Session = Depends(get_db), user=Depends(admin_user)
):
    r = db.query(Restaurant).filter(Restaurant.id == rid).first()
    if not r:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(r)
    db.commit()
    return {"message": "Deleted"}


# Menu CRUD
@router.post("/menu", response_model=MenuItemOut)
def add_menu_item(
    data: MenuItemCreate, db: Session = Depends(get_db), user=Depends(admin_user)
):
    item = MenuItem(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/menu/{item_id}")
def delete_menu_item(
    item_id: int, db: Session = Depends(get_db), user=Depends(admin_user)
):
    item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted"}


# Orders management
@router.get("/orders")
def all_orders(db: Session = Depends(get_db), user=Depends(admin_user)):
    orders = db.query(Order).order_by(Order.created_at.desc()).all()
    return orders


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int, status: str, db: Session = Depends(get_db), user=Depends(admin_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Not found")
    order.status = status
    db.commit()
    return {"message": "Status updated"}


# Users list
@router.get("/users")
def list_users(db: Session = Depends(get_db), user=Depends(admin_user)):
    return db.query(User).all()
