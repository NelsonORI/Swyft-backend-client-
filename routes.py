from flask import Blueprint, request, jsonify
from app import  db  # import the db instance
from models import Customer, Driver, Vehicle, Order, Ride  # import models

# Initialize the Blueprint to organize routes
api = Blueprint('api', __name__)

# Create (Add a new record)
@api.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        full_name=data['full_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        password=data['password']
    )
     db.session.add(new_customer)
     db.session.commit()
    return jsonify({'message': 'Customer created successfully'}), 201

# Read (Fetch records)
@api.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200

# Update (Modify an existing record)
@api.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.get_json()
    customer = Customer.query.get_or_404(id)
    customer.full_name = data.get('full_name', customer.full_name)
    customer.email = data.get('email', customer.email)
    customer.phone_number = data.get('phone_number', customer.phone_number)
     db.session.commit()
    return jsonify({'message': 'Customer updated successfully'}), 200

# Delete (Remove a record)
@api.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
     db.session.delete(customer)
     db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'}), 200
