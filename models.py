from config import db
from sqlalchemy_serializer import SerializerMixin
class Customer(db.Models, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    profile_picture = db.Column(db.String(200))
    password_hash = db.Column(db.String(128), nullable=False)
    
    
    
class Order(db.Models, SerializerMixin):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    distance = db.Column(db.Float, nullable=False)
    loader_number = db.Column(db.Integer(20), nullable=False)
    loader_cost = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    from_location = db.Column(db.String(100), nullable=False)
    to_location = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    
class Vehicle(db.Models, SerializerMixin):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True)
    body_type = db.Column(db.String(50), nullable=False)  # Vehicle body type (e.g., minitruck, pickup, truck)
    plate_no = db.Column(db.String(20), unique=True)
    color = db.Column(db.String(50))
    