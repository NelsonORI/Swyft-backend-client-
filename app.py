import requests
from config import Flask, request, make_response, app, api, Resource, db, session, os, bcrypt, jsonify
from models import Customer, Driver, Vehicle, Order, Rating, Ride
from utils.geocode import geocode
from utils.distance import haversine
    

from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from datetime import timedelta

from confluent_kafka import Producer
import json

# Flask app configurations
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_KEY')
app.config["JWT_TOKEN_LOCATION"] = ['headers']
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
jwt = JWTManager(app)

# Flask app configurations for Jenga API
app.config["JENGA_CONSUMER_KEY"] = "CONSUMER_KEY"
app.config["JENGA_CONSUMER_SECRET"] = "CONSUMER_SECRET"
app.config["JENGA_ENV"] = "sandbox"  # Change to 'production' when live
app.config["JENGA_BASE_URL"] = "https://uat.finserve.africa/v3-apis/payment-api/v3.0/stkussdpush/initiate"  # Update this for production

@jwt.user_identity_loader
def user_identity_lookup(user):
    return {"id": user} 

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    user_id = identity["id"]
    return Customer.query.filter_by(id=user_id).one_or_none()
    
def get_jenga_access_token():
    consumer_key = app.config['JENGA_CONSUMER_KEY']
    consumer_secret = app.config['JENGA_CONSUMER_SECRET']
    auth_url = f"{app.config['JENGA_BASE_URL']}/identity/v2/token"
    
    headers = {
        "Authorization": f"Basic {consumer_key}:{consumer_secret}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {"grant_type": "client_credentials"}
    
    response = requests.post(auth_url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('access_token')
    print(response.status_code, response.text)
    raise Exception('Failed to get Jenga access token')

class JengaPayment(Resource):
    def post(self):
        data = request.get_json()
        phone = data.get('phoneNumber')
        amount = data.get('amount')
        driver_id = data.get('driver_id')
        timestamp = data.get('timestamp')
        
        try:
            access_token = get_jenga_access_token()
            api_url = f"{app.config['JENGA_BASE_URL']}/transaction/v2/remittance"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "source": {
                    "countryCode": "KE",
                    "name": "Your Business Name",
                    "accountNumber": "Source Account Number"
                },
                "destination": {
                    "type": "mobile",
                    "countryCode": "KE",
                    "name": "Recipient Name",
                    "mobileNumber": phone
                },
                "transfer": {
                    "type": "MobileWallet",
                    "amount": str(amount),
                    "currencyCode": "KES",
                    "reference": "PaymentReference",
                    "date": timestamp
                }
            }

            response = requests.post(api_url, json=payload, headers=headers)
            if response.status_code == 200:
                return {'message': 'Payment initiated successfully'}, 200
            return {'error': response.json()}, response.status_code
        except Exception as e:
            return {'error': str(e)}, 500

# Add the new payment resource
api.add_resource(JengaPayment, '/jenga/payment')


    

# Kafka producer configuration
kafka_config = {
    'bootstrap.servers': os.environ.get('KAFKA_SERVERS'),  # Your Kafka broker
    'security.protocol': 'SASL_SSL',  # Ensure this matches Confluent Cloud requirements
    'sasl.mechanisms': 'PLAIN',       # Mechanism used for authentication
    'sasl.username': os.environ.get('KAFKA_USERNAME'),  # Replace with your API key
    'sasl.password': os.environ.get('KAFKA_PASSWORD'),  # Replace with your API secret
    # 'api.version.request': True,     # Ensure the API version is requested
}

producer = Producer(kafka_config)

def delivery_report(err, msg):
    """Delivery report callback for Kafka messages."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return Customer.query.filter_by(id=identity).one_or_none()

class Home(Resource):
    def get(self):
        return {"message": "Welcome to Swyft"}

api.add_resource(Home, '/')

class SignUp(Resource):
    def post(self):
        data = request.get_json()
        
        id = data.get('id')
        full_name = data.get('name')
        email = data.get('email')
        phone_number = data.get('phone')
        password = data.get('password')
        
        
        existing_user = Customer.query.filter(
            (Customer.email == email) | (Customer.phone == phone_number)
        ).first()

        if existing_user:
            if existing_user.email == email:
                return make_response({'error': 'Email already registered, kindly login'}, 400)
            if existing_user.phone == phone_number:
                return make_response({'error': 'Phone number already registered'}, 400)

        try:
            new_user = Customer(
                id=id,
                name=full_name,
                email=email,
                phone=phone_number
            )

            new_user.password_hash = password
            

            db.session.add(new_user)
            db.session.commit()

            response_dict = new_user.to_dict()

            response = make_response(
                {
                    'message':'User created successfully',
                    'user':response_dict,
                    },
                201,
            )

            return response

        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)

api.add_resource(SignUp, '/signup')

class Login(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        existing_user = Customer.query.filter(
            Customer.email == email
        ).first()

        if not existing_user:
            return make_response({'error': 'Email address not found in our records, create account'}, 400)

        if not bcrypt.check_password_hash(existing_user._password_hash, password):
            return make_response({'error': 'Incorrect password, please try again'}, 400)

        access_token = create_access_token(identity=existing_user.id)
        refresh_token = create_refresh_token(identity=existing_user.id)

        response = {
            'access_token': access_token,
            'user':existing_user.to_dict(),
            'refresh_token': refresh_token,
            'message': 'Login successful'
        }

        return make_response(response, 200)

api.add_resource(Login, '/login')

class CheckSession(Resource):
    @jwt_required()
    def get(self):
        return make_response(current_user.to_dict(), 200)

api.add_resource(CheckSession, '/check_session', endpoint="check_session")

class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)

        response = {
            'access_token': new_access_token,
           'message': 'Token refreshed successfully'
        }

        return make_response(response, 200)

api.add_resource(TokenRefresh, '/refresh')

class DriverSignUp(Resource):
    def post(self):
        data = request.get_json()

        id = data.get('id')
        name = data.get('name')
        phone = data.get('phone')
        email = data.get('email')
        car_type = data.get('carType')
        password = data.get('password')
        license_number = data.get('licenseNumber')
        id_number = data.get('idNumber')
        license_plate = data.get('licensePlate')

        existing_driver = Driver.query.filter(
            (Driver.email == email) | (Driver.phone == phone)
        ).first()

        if existing_driver:
            if existing_driver.email == email:
                return make_response({'error':'Email already registered, kindly login'}, 400)
            if existing_driver.phone == phone:
                return make_response({'error':'Phone number already registered'}, 400)

        duplicate_driver = Driver.query.filter(
            (Driver.id_number == id_number) |
            (Driver.license_number == license_number) |
            (Driver.license_plate == license_plate)
        ).first()

        if duplicate_driver:
            if duplicate_driver.id_number == id_number:
                return make_response({'error':'Driver already registered'}, 400)
            if duplicate_driver.license_number == license_number:
                return make_response({'error':'Driver already registered'}, 400)
            if duplicate_driver.license_plate == license_plate:
                return make_response({'error':'Driver already registered'}, 400)

        try:
            new_driver = Driver(
                id=id,
                name=name,
                phone=phone,
                email=email,
                car_type=car_type,
                license_number=license_number,
                id_number=id_number,
                license_plate=license_plate
            )

            new_driver.password_hash = password

            db.session.add(new_driver)
            db.session.commit()

            return make_response({'message':'Driver created successfully'}, 201)

        except IntegrityError as e:
            db.session.rollback()
            return make_response({'error':'An error occured while registering the driver:' + str(e)}, 500)
        except Exception as e:
            db.session.rollback()
            return make_response({'error':'An error occured: ' + str(e)}, 500)

api.add_resource(DriverSignUp,'/driver/signup')


class DriverLogin(Resource):
    def post(self):
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')

        existing_driver = Driver.query.filter(Driver.email == email).first()

        if not existing_driver:
            return make_response({'error':'Email address not found in our records, create account'}, 400)

        if not bcrypt.check_password_hash(existing_driver._password_hash,password):
            return make_response({'error':'Incorrect password, please try again'}, 400)

        access_token = create_access_token(identity=existing_driver.id)
        refresh_token = create_refresh_token(identity=existing_driver.id)


        response = {
            'access_token':access_token,
            'refresh_token':refresh_token,
            'message':'Login successful'
        }

        return make_response(response,200)

api.add_resource(DriverLogin,'/driver/login')

class OrderResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        orders = Order.query.filter_by(customer_id=current_user_id).all()
        if not orders:
            return make_response({'message': 'No orders found'}, 200)
        response = [order.to_dict() for order in orders]
        return make_response(response, 200)

    @jwt_required()
    def post(self):
        data = request.get_json()
        customer_id = get_jwt_identity()

        vehicle = data.get('vehicle')
        distance = data.get('distance')
        loaders = data.get('loaders')
        loader_cost = data.get('loaderCost')
        total_cost = data.get('totalCost')
        user_location = data.get('userLocation')
        destination = data.get('destination')
        time = data.get('time')

        if not all([user_location,destination]):
            return make_response({'error':'Pickup and drop-off locations are required'}, 400)

        from_latitude = user_location.get('lat')
        from_longitude = user_location.get('lng')
        to_latitude = destination.get('lat')
        to_longitude = destination.get('lng')

        if not all([from_latitude, from_longitude, to_latitude, to_longitude]):
            return make_response({'error': 'Invalid coordinates provided for pickup or destination'}, 400)

        drivers = Driver.query.filter_by(online=True, car_type = vehicle).all()
        if not drivers:
            return make_response({'error':'No available driver with the requested vehicle type'}, 404)

        try:
            nearest_driver = None 
            min_distance = float('inf')

            for driver in drivers:
                driver_distance = haversine(from_latitude,from_longitude,driver.latitude,driver.longitude)
                if driver_distance < min_distance:
                    min_distance = driver_distance
                    nearest_driver = driver

            if not nearest_driver:
                return make_response({'error':'No available drivers nearby'}, 404)

            order_data = {
                "customer_id":customer_id,
                "from_location":user_location,
                "to_location":destination,
                "distance":data.get('distance'),
                "loader_number":data.get('loader_number'),
                "loader_cost":data.get('loader_cost'),
                "price":data.get('price'),
                "driver_id":nearest_driver.id,
                "vehicle_type": data.get('vehicle'),
            }

            new_order = Order(
                id=data.get('id'),
                customer_id=customer_id,
                vehicle_type = data.get('vehicle'),
                distance=data.get('distance'),
                loaders=data.get('loaders'),
                loader_cost=data.get('loaderCost'),
                total_cost=data.get('totalCost'),
                user_lat=from_latitude,
                user_lng=from_longitude,
                dest_lat=to_latitude,
                dest_lng=to_longitude,
                time=data.get('time') ,        
                driver_id=nearest_driver.id
            )
            db.session.add(new_order)
            db.session.commit()
            

                # Send order data to Kafka
            producer.produce(
                'order-topic',  # Kafka topic
                key=str(new_order.id),
                value=json.dumps(order_data),
                callback=delivery_report
            )
            producer.flush()

            return make_response({'message': 'Order made successfully','nearest_driver':nearest_driver.to_dict()}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)

    @jwt_required()
    def put(self, order_id):
        current_user_id = get_jwt_identity()
        data = request.get_json()

        order = Order.query.get(order_id)
        if not order:
            return make_response({'message': 'Order not found'}, 404)

        if order.customer_id != current_user_id:
            return make_response({'error': 'Unauthorized to update this order'}, 403)

        try:
            new_user_location = data.get('userLocation', {})
            new_destination = data.get('destination', {})

            if new_user_location or new_destination:
                from_latitude = new_user_location.get('lat',order.user_lat)
                from_longitude = new_user_location.get('lng', order.user_lng)
                to_latitude = new_destination.get('lat', order.dest_lat)
                to_longitude = new_destination.get('lng', order.dest_lng)

                if not all([from_latitude, from_longitude, to_latitude, to_longitude]):
                    return make_response({'error': 'Invalid coordinates provided for pickup or destination'}, 400)

                order.user_lat = from_latitude
                order.user_lng = from_longitude
                order.dest_lat = to_latitude
                order.dest_lng = to_longitude

                new_vehicle = data.get('vehicle', order.vehicle_type)
                if new_vehicle!= order.vehicle_type:
                    drivers = Driver.query.filter_by(online=True, car_type=new_vehicle).all()
                    if not drivers:
                        return make_response({'error':'No available driver with the requested vehicle type'}, 404)

                    nearest_driver = None
                    min_distance = float('inf')
                    for driver in drivers:
                        driver_distance = haversine(order.user_lat, order.user_lng, driver.latitude, driver.longitude)
                        if driver_distance < min_distance:
                            min_distance = driver_distance
                            nearest_driver = driver

                    if not nearest_driver:
                        return make_response({'error':'No available drivers nearby'}, 404)

                    order.driver_id = nearest_driver.id
                    order.vehicle_type = new_vehicle
                
                order.distance = data.get('distance', order.distance)
                order.loaders = data.get('loaders', order.loaders)
                order.loader_cost = data.get('loaderCost', order.loader_cost)
                order.total_cost = data.get('totalCost', order.total_cost)
                order.time = data.get('time', order.time)

                db.session.commit()

                updated_order_data = {
                    "customer_id": order.customer_id,
                    "from_location": {"lat": order.user_lat, "lng": order.user_lng},
                    "to_location": {"lat": order.dest_lat, "lng": order.dest_lng},
                    "distance": order.distance,
                    "loaders": order.loaders,
                    "loader_cost": order.loader_cost,
                    "price": order.total_cost,
                    "driver_id": order.driver_id,
                    "vehicle_type": order.vehicle_type
                }

                producer.produce(
                    'order-topic',
                    key=str(order.id),
                    value=json.dumps(updated_order_data),
                    callback=delivery_report
                )
                producer.flush()

                return make_response({'message': 'Order updated successfully','order': order.to_dict()}, 200)

        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)
            

    @jwt_required()
    def delete(self, order_id):
        current_user_id = get_jwt_identity()
        order = Order.query.get(order_id)
        if not order:
            return make_response({'error': 'Order not found'}, 404)

        if order.customer_id != current_user_id:
            return make_response({'error': 'Unauthorized to delete this order'}, 403)

        try:
            db.session.delete(order)
            db.session.commit()
            return make_response({'message': 'Order deleted successfully'}, 200)
        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)

api.add_resource(OrderResource, '/orders', '/orders/<string:order_id>')


class Drivers(Resource):
    def post(self):
        data = request.get_json()

        email = data.get('email')
        phone_number = data.get('phone_number')

        existing_user = Driver.query.filter(
            (Driver.email == email) | (Driver.phone_number == phone_number)
        ).first()

        if existing_user:
            if existing_user.email == email:
                return make_response({'error':'Email already registered, kindly login'}, 400)
            if existing_user.phone_number == phone_number:
                return make_response({'error':'Phone number already registered'}, 400)

        driver_base = data.get('driver_base')
        driver_base_coords = geocode(driver_base)
        
        if not driver_base_coords:
            return make_response({'error':'Unable to geocode location provided. Please check the address'}, 400)

        latitude, longitude = driver_base_coords
        try: 
            new_driver = Driver(
                name=data.get('name'),
                id_number=data.get('id'),
                driving_license_no=data.get('dl_no'),
                profile_picture=data.get('profile_picture'),
                driver_base=data.get('driver_base'),
                email=data.get('email'),
                phone_number=data.get('phone_number'),
                latitude=latitude,
                longitude=longitude
            )
            db.session.add(new_driver)
            db.session.commit()

            return make_response({'message':'Driver registered successfully'}, 200)

        except Exception as e:
            db.session.rollback()
            return make_response({'error':str(e)}, 500)

api.add_resource(Drivers,'/driver/signup')

class UpdateDriverLocation(Resource):
    def put(self, driver_id):
        data = request.get_json()

        location = data.get('location')
        if location is None:
            return make_response({'error': 'Location is required'}, 400)

        latitude = location.get('latitude')
        longitude = location.get('longitude')

        driver = Driver.query.get(driver_id)
        if not driver:
            return make_response({'error': 'Driver not found'}, 404)

        if driver.online:
            driver.online = False
            message = "You are now offline"
        else:
            driver.online = True
            driver.latitude = latitude
            driver.longitude = longitude
            message = "You are now online"
            
        db.session.commit()
        return make_response({
            'message': message,
            'online_status':driver.online
        }, 200)

api.add_resource(UpdateDriverLocation,'/online/<string:driver_id>')
            

if __name__ == '__main__':
    app.run(debug=True)
