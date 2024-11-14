from config import app, db
from models import Customer, Driver, Vehicle, Order, Rating, Ride

with app.app_context():
    # Drop all tables and recreate them
    print("Resetting database...")
    db.drop_all()
    db.create_all()

    # Seed data for Customers
    customers = [
        Customer(full_name="John Doe", email="john.doe@example.com", phone_number="1234567890", profile_picture="profile1.jpg"),
        Customer(full_name="Jane Smith", email="jane.smith@example.com", phone_number="0987654321", profile_picture="profile2.jpg")
    ]

    customers[0].password_hash = "password1"
    customers[1].password_hash = "password2"
    db.session.add_all(customers)

    # Seed data for Drivers
    drivers = [
        Driver(name="Tom Driver", id_no="ID12345", driving_license_no="DL12345", profile_picture="driver1.jpg"),
        Driver(name="Sara Wheels", id_no="ID67890", driving_license_no="DL67890", profile_picture="driver2.jpg")
    ]

    db.session.add_all(drivers)

    # Seed data for Vehicles
    vehicles = [
        Vehicle(body_type="Sedan", plate_no="ABC123", driver_id=1),
        Vehicle(body_type="Truck", plate_no="XYZ789", driver_id=2)
    ]

    db.session.add_all(vehicles)

    # Seed data for Orders
    orders = [
        Order(distance=15.5, loader_number=2, loader_cost=50.0, from_location="Location A", to_location="Location B", price=200.0, customer_id=1, driver_id=1),
        Order(distance=30.0, loader_number=3, loader_cost=75.0, from_location="Location C", to_location="Location D", price=400.0, customer_id=2, driver_id=2)
    ]

    db.session.add_all(orders)

    # Seed data for Rides
    rides = [
    Ride(distance=15.5, loader_cost=50.0, from_location='Location A', to_location='Location B', price=100.0, order_id=1),
    Ride(distance=30.0, loader_cost=80.0, from_location='Location C', to_location='Location D', price=150.0, order_id=2)
]


    db.session.add_all(rides)

    # Seed data for Ratings
    ratings = [
        Rating(rating_score=5, order_id=1, ride_id=1),
        Rating(rating_score=4, order_id=2, ride_id=2)
    ]

    db.session.add_all(ratings)

    # Commit the changes to the database
    print("Committing seed data to the database...")
    db.session.commit()

    print("Database seeded successfully!")
