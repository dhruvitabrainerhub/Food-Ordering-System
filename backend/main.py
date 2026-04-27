from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from routers import admin, auth, orders, payment, users

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
