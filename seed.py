from config import db, bcrypt, app
from models import Customer, Driver, Vehicle, Order, Rating, Ride

with app.app_context():
    print("Dropping all tables ")
    db.drop_all()
    print("Creating new tables")
    db.create_all()