from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    profile_picture = db.Column(db.String(200))
    
    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self,password):
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash,password.encode("utf-8"))
    
    orders = db.relationship('Order', backref='customer', lazy=True)

    serialize_rules = ('-password', '-_password_hash', '-orders')



class Driver(db.Model, SerializerMixin):
    __tablename__ = 'drivers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =  db.Column( db.String(100), nullable=False)
    id_no =  db.Column( db.String(20), unique=True, nullable=False)
    driving_license_no =  db.Column( db.String(20), unique=True, nullable=False)
    profile_picture =  db.Column( db.String(200))
    created_at =  db.Column( db.DateTime, default= db.func.current_timestamp())
    
    # Define relationship to Vehicle
    vehicle =  db.relationship('Vehicle', backref='driver', lazy=True, uselist=False)


class Vehicle(db.Model, SerializerMixin):
    __tablename__ = 'vehicles'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body_type = db.Column(db.String(50), nullable=False)
    plate_no = db.Column(db.String(20), unique=True, nullable=False)
    
    
    # Foreign key to Driver
    driver_id =  db.Column( db.Integer,  db.ForeignKey('drivers.id'))
    customers_id =  db.Column( db.Integer,  db.ForeignKey('customers.id'))

class Order( db.Model, SerializerMixin):
    __tablename__ = 'orders'
    
    id =  db.Column( db.Integer, primary_key=True, autoincrement=True)
    distance =  db.Column( db.Float, nullable=False)
    loader_number =  db.Column( db.Integer, nullable=False)
    loader_cost =  db.Column( db.Float, nullable=False)
    from_location =  db.Column( db.String(100), nullable=False)
    to_location =  db.Column( db.String(100), nullable=False)
    price =  db.Column( db.Float, nullable=False)
    created_at =  db.Column( db.DateTime, default= db.func.current_timestamp())
    
    # Foreign keys to Customer and Driver
    customer_id =  db.Column( db.Integer,  db.ForeignKey('customers.id'))
    driver_id =  db.Column( db.Integer,  db.ForeignKey('drivers.id'))


class Rating( db.Model, SerializerMixin):
    __tablename__ = 'ratings'
    
    id =  db.Column( db.Integer, primary_key=True, autoincrement=True)
    rating_score =  db.Column( db.Integer, nullable=False)
    
    # Foreign keys to Order and Ride
    order_id =  db.Column( db.Integer,  db.ForeignKey('orders.id'))
    ride_id =  db.Column( db.Integer,  db.ForeignKey('rides.id'))


class Ride( db.Model, SerializerMixin):
    __tablename__ = 'rides'
    
    id =  db.Column( db.Integer, primary_key=True, autoincrement=True)
    distance =  db.Column( db.Float, nullable=False)
    created_time =  db.Column( db.DateTime, default= db.func.current_timestamp())
    loader_cost =  db.Column( db.Float, nullable=False)
    from_location =  db.Column( db.String(100), nullable=False)
    to_location =  db.Column( db.String(100), nullable=False)
    price =  db.Column( db.Float, nullable=False)
    
    # Foreign key to Order
    order_id =  db.Column( db.Integer,  db.ForeignKey('orders.id'))
