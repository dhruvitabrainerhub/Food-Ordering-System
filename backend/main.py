from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import auth, users, orders, admin, payment

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Order API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(admin.router)
app.include_router(payment.router)

@app.get("/")
def root():
    return {"message": "Food Order API Running"}
