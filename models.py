from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    
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

    vehicles = db.relationship('Vehicle', backref='customer', lazy='dynamic')



class Driver(db.Model, SerializerMixin):
    __tablename__ = 'drivers'

    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    car_type = db.Column(db.String(100), nullable=False)
    online = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float(), default=0, nullable=False)
    longitude = db.Column(db.Float(), default=0, nullable=False)

    _password_hash = db.Column(db.String(128), nullable=False)

    license_number = db.Column(db.String(100), nullable=False)
    id_number = db.Column(db.String(100), nullable=False)
    license_plate = db.Column(db.String(100), nullable=False)

    orders = db.relationship('Order', backref = 'driver', lazy = True)

    @hybrid_property
    def password_hash(self):
         """Password hashes should not be viewed directly"""
         raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        """Hash the password before storing it."""
        password_hash = bcrypt.generate_password_hash(password.encode("utf-8"))
        self._password_hash = password_hash.decode("utf-8")

    def authenticate(self, password):
        """Authenticate the password by comparing the input password with the stored hash."""
        return bcrypt.check_password_hash(self._password_hash, password.encode("utf-8"))

    serialize_rules = ('-password', '-_password_hash')

class Vehicle(db.Model, SerializerMixin): 
    __tablename__ = 'vehicles'
    
    id = db.Column(db.String(100), primary_key=True)
    body_type = db.Column(db.String(50), nullable=False)
    plate_no = db.Column(db.String(20), unique=True, nullable=False)
    
    
    # Foreign key to Driver
    driver_id =  db.Column( db.String(100),  db.ForeignKey('drivers.id'))
    customer_id =  db.Column( db.String(100),  db.ForeignKey('customers.id'))

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.String(100), primary_key=True)  # Match the "id" from frontend
    vehicle_type = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    loaders = db.Column(db.Integer, nullable=False, default=0)
    loader_cost = db.Column(db.Float, nullable=False, default=0.0)
    total_cost = db.Column(db.Float, nullable=False)
    user_lat = db.Column(db.Float, nullable=False)  # Latitude for user location
    user_lng = db.Column(db.Float, nullable=False)  # Longitude for user location
    dest_lat = db.Column(db.Float, nullable=False)  # Latitude for destination
    dest_lng = db.Column(db.Float, nullable=False)  # Longitude for destination
    time = db.Column(db.String(100), nullable=False)  # Store as string or datetime
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # For tracking

    # Optional: Relationship to Driver if needed
    driver_id = db.Column(db.String(100), db.ForeignKey('drivers.id'))
    customer_id = db.Column(db.String(100), db.ForeignKey('customers.id'))
    
    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_type": self.vehicle_type,
            "distance": self.distance,
            "loaders": self.loaders,
            "loader_cost": self.loader_cost,
            "total_cost": self.total_cost,
            "user_lat": self.user_lat,
            "user_lng": self.user_lng,
            "dest_lat": self.dest_lat,
            "dest_lng": self.dest_lng,
            "time": self.time,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            "driver_id": self.driver_id,
            "customer_id": self.customer_id,
        }



class Rating( db.Model, SerializerMixin):
    __tablename__ = 'ratings'
    
    id =  db.Column( db.String(100), primary_key=True)
    rating_score =  db.Column( db.Integer, nullable=False)
    
    # Foreign keys to Order and Ride
    order_id =  db.Column( db.String(100),  db.ForeignKey('orders.id'))
    ride_id =  db.Column( db.String(100),  db.ForeignKey('rides.id'))


class Ride( db.Model, SerializerMixin):
    __tablename__ = 'rides'
    
    id =  db.Column( db.String(100), primary_key=True)
    distance =  db.Column( db.Float, nullable=False)
    created_time =  db.Column( db.DateTime, default= db.func.current_timestamp())
    loader_cost =  db.Column( db.Float, nullable=False)
    from_location =  db.Column( db.String(100), nullable=False)
    to_location =  db.Column( db.String(100), nullable=False)
    price =  db.Column( db.Float, nullable=False)
    
    # Foreign key to Order
    order_id =  db.Column( db.String(100),  db.ForeignKey('orders.id'))
