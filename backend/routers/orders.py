from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database import get_db
from models import Order, OrderItem
from routers.auth import get_current_user
from schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/orders", tags=["orders"])
security = HTTPBearer()


def auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    return get_current_user(credentials.credentials, db)


@router.post("/", response_model=OrderOut)
def place_order(
    order: OrderCreate, db: Session = Depends(get_db), user=Depends(auth_user)
):
    new_order = Order(
        user_id=user.id,
        restaurant_id=order.restaurant_id,
        total_amount=order.total_amount,
        address=order.address,
    )
    db.add(new_order)
    db.flush()
    for item in order.items:
        db.add(
            OrderItem(
                order_id=new_order.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                price=item.price,
            )
        )
    db.commit()
    db.refresh(new_order)
    return new_order


@router.get("/my", response_model=List[OrderOut])
def my_orders(db: Session = Depends(get_db), user=Depends(auth_user)):
    return (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


@router.put("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db), user=Depends(auth_user)):
    order = (
        db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in ["pending", "confirmed", "preparing"]:
        raise HTTPException(status_code=400, detail="Cannot cancel this order")
    order.status = "cancelled"
    db.commit()
    return {"message": "Order cancelled"}


@router.put("/{order_id}/confirm")
def confirm_order(
    order_id: int, db: Session = Depends(get_db), user=Depends(auth_user)
):
    order = (
        db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = "confirmed"
    db.commit()
    return {"message": "Order confirmed"}
