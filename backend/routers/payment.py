from fastapi import APIRouter, HTTPException, Request, Header, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models import Order
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

router = APIRouter(prefix="/payment", tags=["payment"])

class CheckoutRequest(BaseModel):
    order_id: int
    amount: float
    success_url: str
    cancel_url: str

@router.get("/publishable-key")
def get_publishable_key():
    return {"publishable_key": os.getenv("STRIPE_PUBLISHABLE_KEY")}

@router.post("/create-checkout")
def create_checkout_session(data: CheckoutRequest):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "inr",
                    "product_data": {"name": f"FoodExpress Order #{data.order_id}"},
                    "unit_amount": int(data.amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=data.success_url + f"?session_id={{CHECKOUT_SESSION_ID}}&order_id={data.order_id}",
            cancel_url=data.cancel_url,
            metadata={"order_id": str(data.order_id)}
        )
        return {"checkout_url": session.url, "session_id": session.id}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e.user_message))

@router.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None), db: Session = Depends(get_db)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(payload, stripe_signature, WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        order_id = session.get("metadata", {}).get("order_id")
        if order_id:
            order = db.query(Order).filter(Order.id == int(order_id)).first()
            if order:
                order.status = "confirmed"
                db.commit()

    elif event["type"] == "checkout.session.expired":
        session = event["data"]["object"]
        order_id = session.get("metadata", {}).get("order_id")
        if order_id:
            order = db.query(Order).filter(Order.id == int(order_id)).first()
            if order:
                order.status = "cancelled"
                db.commit()

    return {"status": "ok"}
