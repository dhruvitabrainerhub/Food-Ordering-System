"""Run this once to create admin user and sample data"""

from passlib.context import CryptContext

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()
pwd = CryptContext(schemes=["bcrypt"])

# Create admin user
if not db.query(models.User).filter(models.User.email == "admin@food.com").first():
    admin = models.User(
        name="Admin",
        email="admin@food.com",
        password=pwd.hash("admin123"),
        phone="9999999999",
        is_admin=True,
    )
    db.add(admin)
    db.commit()
    print("[OK] Admin created: admin@food.com / admin123")

# Sample restaurants
if not db.query(models.Restaurant).first():
    restaurants = [
        models.Restaurant(
            name="Spice Garden",
            description="Authentic Indian cuisine",
            cuisine="Indian",
            delivery_time="30-40 mins",
            rating=4.5,
            image="https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400",
        ),
        models.Restaurant(
            name="Pizza Palace",
            description="Best pizzas in town",
            cuisine="Italian",
            delivery_time="25-35 mins",
            rating=4.3,
            image="https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
        ),
        models.Restaurant(
            name="Burger Hub",
            description="Juicy burgers & fries",
            cuisine="American",
            delivery_time="20-30 mins",
            rating=4.1,
            image="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400",
        ),
    ]
    for r in restaurants:
        db.add(r)
    db.commit()

    # Sample menu items
    r1, r2, r3 = db.query(models.Restaurant).all()
    items = [
        models.MenuItem(
            restaurant_id=r1.id,
            name="Butter Chicken",
            description="Creamy tomato curry",
            price=280,
            category="Main Course",
        ),
        models.MenuItem(
            restaurant_id=r1.id,
            name="Paneer Tikka",
            description="Grilled cottage cheese",
            price=220,
            category="Starters",
        ),
        models.MenuItem(
            restaurant_id=r1.id,
            name="Dal Makhani",
            description="Slow cooked black lentils",
            price=180,
            category="Main Course",
        ),
        models.MenuItem(
            restaurant_id=r2.id,
            name="Margherita Pizza",
            description="Classic tomato & cheese",
            price=350,
            category="Pizza",
        ),
        models.MenuItem(
            restaurant_id=r2.id,
            name="Pepperoni Pizza",
            description="Loaded with pepperoni",
            price=420,
            category="Pizza",
        ),
        models.MenuItem(
            restaurant_id=r3.id,
            name="Classic Burger",
            description="Beef patty with veggies",
            price=199,
            category="Burgers",
        ),
        models.MenuItem(
            restaurant_id=r3.id,
            name="Cheese Fries",
            description="Crispy fries with cheese",
            price=120,
            category="Sides",
        ),
    ]
    for item in items:
        db.add(item)
    db.commit()
    print("[OK] Sample restaurants and menu items created!")

db.close()
print("[OK] Database ready!")
