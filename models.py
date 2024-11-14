from extensions import swyft_db
from sqlalchemy_serializer import SerializerMixin

class Customer(swyft_db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = swyft_db.Column(swyft_db.Integer, primary_key=True, autoincrement=True)
    full_name = swyft_db.Column(swyft_db.String(100), nullable=False)
    email = swyft_db.Column(swyft_db.String(100), unique=True, nullable=False)
    phone_number = swyft_db.Column(swyft_db.String(20), unique=True, nullable=False)
    password = swyft_db.Column(swyft_db.String(128), nullable=False)
    profile_picture = swyft_db.Column(swyft_db.String(200))
    
    orders = swyft_db.relationship('Order', backref='customer', lazy=True)


class Driver(swyft_db.Model, SerializerMixin):
    __tablename__ = 'drivers'
    
    id = swyft_db.Column(swyft_db.Integer, primary_key=True, autoincrement=True)
    name = swyft_db.Column(swyft_db.String(100), nullable=False)
    id_no = swyft_db.Column(swyft_db.String(20), unique=True, nullable=False)
    driving_license_no = swyft_db.Column(swyft_db.String(20), unique=True, nullable=False)
    profile_picture = swyft_db.Column(swyft_db.String(200))
    created_at = swyft_db.Column(swyft_db.DateTime, default=swyft_db.func.current_timestamp())
    
    # Define relationship to Vehicle
    vehicle = swyft_db.relationship('Vehicle', backref='driver', lazy=True, uselist=False)


class Vehicle(swyft_db.Model, SerializerMixin):
    __tablename__ = 'vehicles'
    
    id = swyft_db.Column(swyft_db.Integer, primary_key=True, autoincrement=True)
    body_type = swyft_db.Column(swyft_db.String(50), nullable=False)
    plate_no = swyft_db.Column(swyft_db.String(20), unique=True, nullable=False)
    
    
    # Foreign key to Driver
    driver_id = swyft_db.Column(swyft_db.Integer, swyft_db.ForeignKey('drivers.id'))
    customers_id = swyft_db.Column(swyft_db.Integer, swyft_db.ForeignKey('customers.id'))

class Order(swyft_db.Model, SerializerMixin):
    __tablename__ = 'orders'
    
    id = swyft_db.Column(swyft_db.Integer, primary_key=True, autoincrement=True)
    distance = swyft_db.Column(swyft_db.Float, nullable=False)
    loader_number = swyft_db.Column(swyft_db.Integer, nullable=False)
    loader_cost = swyft_db.Column(swyft_db.Float, nullable=False)
    from_location = swyft_db.Column(swyft_db.String(100), nullable=False)
    to_location = swyft_db.Column(swyft_db.String(100), nullable=False)
    price = swyft_db.Column(swyft_db.Float, nullable=False)
    created_at = swyft_db.Column(swyft_db.DateTime, default=swyft_db.func.current_timestamp())
    
    # Foreign keys to Customer and Driver
    customer_id = swyft_db.Column(swyft_db.Integer, swyft_db.ForeignKey('customers.id'))
    driver_id = swyft_db.Column(swyft_db.Integer, swyft_db.ForeignKey('drivers.id'))


class Rating(swyft_db.Model, SerializerMixin):
    __tablename__ = 'ratings'
    
    id = swyft_db.Column(swyft_db.Integer, primary_key=True, autoincrement=True)
    rating_score = swyft_db.Column(swyft_db.Integer, nullable=False)
    
    # Foreign keys to Order and Ride
    order_id = swyft_db.Column(swyft_db.Integer, swyft_db.ForeignKey('orders.id'))
    ride_id = swyft_db.Column(swyft_db.Integer, swyft_db.ForeignKey('rides.id'))


class Ride(swyft_db.Model, SerializerMixin):
    __tablename__ = 'rides'
    
    id = swyft_db.Column(swyft_db.Integer, primary_key=True, autoincrement=True)
    distance = swyft_db.Column(swyft_db.Float, nullable=False)
    created_time = swyft_db.Column(swyft_db.DateTime, default=swyft_db.func.current_timestamp())
    loader_cost = swyft_db.Column(swyft_db.Float, nullable=False)
    from_location = swyft_db.Column(swyft_db.String(100), nullable=False)
    to_location = swyft_db.Column(swyft_db.String(100), nullable=False)
    price = swyft_db.Column(swyft_db.Float, nullable=False)
    
    # Foreign key to Order
    order_id = swyft_db.Column(swyft_db.Integer, swyft_db.ForeignKey('orders.id'))
