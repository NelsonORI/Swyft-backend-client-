from config import Flask, request, make_response, app, api, Resource, db, session, os, request, bcrypt, jsonify
from models import Customer, Driver, Vehicle, Order, Rating, Ride

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity,current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_KEY')
app.config["JWT_TOKEN_LOCATION"] = ['headers']
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header,jwt_data):
    identity = jwt_data["sub"]
    return Customer.query.filter_by(id=identity).one_or_none()

class Home(Resource):
    def get(self):
        return{"message":"Welcome to Swyft"}

api.add_resource(Home, '/')

class SignUp(Resource):
   def post(self):

    data = request.get_json()

    full_name = data.get('full_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')
    profile_picture = data.get('profile_picture')
    
    existing_user = Customer.query.filter(
        (Customer.email == email) | (Customer.phone_number == phone_number)
    ).first()

    if existing_user:
        if existing_user.email == email:
            return make_response({'error':'Email already registered, kindly login'}, 400)
        if existing_user.phone_number == phone_number:
            return make_response({'error':'Phone number already registered'}, 400)

    try:
        new_user = Customer(
            full_name = full_name,
            email = email,
            phone_number = phone_number,
            profile_picture = profile_picture
        )

        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        response_dict = new_user.to_dict()

        response = make_response(
            response_dict,
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
                return make_response({'error':'Email address not found in our records, create account'}, 400)

        if not bcrypt.check_password_hash(existing_user._password_hash, password):
            return make_response({'error':'Incorrect password, please try again'}, 400)

        access_token = create_access_token(identity = existing_user.id)

        response = {
            'access_token':  access_token,
            'message': 'Login successful'
        }

        return make_response(response, 200)

api.add_resource(Login, '/login')

class OrderResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        orders = Order.query.filter_by(customer_id = current_user_id).all()
        if not orders:
            return make_response({'message':'No orders found'}, 200)
        response = [order.to_dict() for order in orders]
        return make_response(response,200)

    @jwt_required()
    def post(self):
        data = request.get_json()
        customer_id = get_jwt_identity()
        try:
            new_order = Order(
                customer_id = customer_id,
                distance = data.get('distance'),
                loader_number = data.get('loader_number'),
                loader_cost = data.get('loader_cost'),
                from_location = data.get('from_location'),
                to_location = data.get('to_location'),
                price = data.get('price')
            )
            db.session.add(new_order)
            db.session.commit()
            return make_response({'message':'Order made sucessfully'},200)
        except Exception as e:
            db.session.rollback()
            return make_response({'error':str(e)}, 500)
    
    @jwt_required()
    def put(self,order_id):
        data = request.get_json()
        order = Order.query.get(order_id)
        if not order:
            return make_response({'message':'Order not found'}, 404)
        try:
            order.distance = data.get('distance',order.distance)
            order.loader_number = data.get('loader_number',order.loader_number)
            order.loader_cost = data.get('loader_cost',order.loader_cost)
            order.from_location = data.get('from_location',order.from_location)
            order.to_location = data.get('to_location',order.to_location)
            order.price = data.get('price',order.price)
            db.session.commit()
            return make_response({'message':'Order updated successfully'}, 200)
        
        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)

    @jwt_required()
    def delete(self,order_id):
        current_user_id = get_jwt_identity()
        order = Order.query.get(order_id)
        if not order:
            return make_response({'error':'Order not found'}, 404)

        if order.customer_id != current_user_id:
            return make_response({'error':'Unauthorized'},403)

        try:
            db.session.delete(order)
            db.session.commit()
            return make_response({'message':'Order deleted successfully'}, 200)

        except Exception as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)



api.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')



if __name__ == '__main__':
    app.run(debug=True)
