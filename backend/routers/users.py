from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import MenuItem, Restaurant
from schemas import MenuItemOut, RestaurantOut

router = APIRouter(tags=["users"])


@router.get("/restaurants", response_model=List[RestaurantOut])
def get_restaurants(db: Session = Depends(get_db)):
    return db.query(Restaurant).filter(Restaurant.is_active.is_(True)).all()


@router.get("/restaurants/{restaurant_id}/menu", response_model=List[MenuItemOut])
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return (
        db.query(MenuItem)
        .filter(
            MenuItem.restaurant_id == restaurant_id, MenuItem.is_available.is_(True)
        )
        .all()
    )


@router.get("/restaurants/{restaurant_id}", response_model=RestaurantOut)
def get_restaurant(restaurant_id: int, db: Session = Depends(get_db)):
    r = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return r
