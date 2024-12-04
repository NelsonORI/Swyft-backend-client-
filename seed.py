# from config import db, bcrypt, app
# from models import Customer, Driver, Vehicle, Order, Rating, Ride
# import random
# from datetime import datetime

# with app.app_context():
    
#     # Function to create sample data
#     def seed_database():
#         # Clear existing data
#         db.session.query(Rating).delete()
#         db.session.query(Ride).delete()
#         db.session.query(Order).delete()
#         db.session.query(Vehicle).delete()
#         db.session.query(Driver).delete()
#         db.session.query(Customer).delete()
#         db.session.commit()

#     #     # Seed Customers
#     #     customers = [
#     #         Customer(
#     #             full_name="John Doe",
#     #             email="john.doe@example.com",
#     #             phone_number="1234567890",
#     #             profile_picture="profile1.jpg",
#     #             password_hash="password123"
#     #         ),
#     #         Customer(
#     #             full_name="Jane Smith",
#     #             email="jane.smith@example.com",
#     #             phone_number="0987654321",
#     #             profile_picture="profile2.jpg",
#     #             password_hash="securepassword"
#     #         )
#     #     ]
#     #     for customer in customers:
#     #         customer.password_hash = customer.password_hash  # Hash the passwords
#     #         db.session.add(customer)

#     #     # Seed Drivers
#     #     drivers = [
#     #         Driver(
#     #             name="Michael Johnson",
#     #             id_no="12345678",
#     #             driving_license_no="DL12345",
#     #             profile_picture="driver1.jpg",
#     #             driver_base="Nairobi",
#     #             email="michael.johnson@example.com",
#     #             phone_number="2345678901",
#     #             latitude=-1.286389,
#     #             longitude=36.817223
#     #         ),
#     #         Driver(
#     #             name="Sarah Connor",
#     #             id_no="87654321",
#     #             driving_license_no="DL54321",
#     #             profile_picture="driver2.jpg",
#     #             driver_base="Mombasa",
#     #             email="sarah.connor@example.com",
#     #             phone_number="3456789012",
#     #             latitude=-4.043477,
#     #             longitude=39.668206
#     #         )
#     #     ]
#     #     for driver in drivers:
#     #         db.session.add(driver)

#     #     # Seed Vehicles
#     #     vehicles = [
#     #         Vehicle(
#     #             body_type="Van",
#     #             plate_no="KAB123A",
#     #             driver_id=1,  # Assuming Driver IDs start from 1
#     #             customers_id=1
#     #         ),
#     #         Vehicle(
#     #             body_type="Truck",
#     #             plate_no="KAC456B",
#     #             driver_id=2,
#     #             customers_id=2
#     #         )
#     #     ]
#     #     for vehicle in vehicles:
#     #         db.session.add(vehicle)

#     #     # Seed Orders
#     #     orders = [
#     #         Order(
#     #             id="ORD123",
#     #             vehicle_type="Van",
#     #             distance=12.5,
#     #             loaders=2,
#     #             loader_cost=300,
#     #             total_cost=2500,
#     #             user_lat=-1.286389,
#     #             user_lng=36.817223,
#     #             dest_lat=-1.292065,
#     #             dest_lng=36.821946,
#     #             time="2024-11-25 10:00",
#     #             driver_id=1,
#     #             customer_id=1
#     #         ),
#     #         Order(
#     #             id="ORD124",
#     #             vehicle_type="Truck",
#     #             distance=25.0,
#     #             loaders=3,
#     #             loader_cost=450,
#     #             total_cost=5000,
#     #             user_lat=-4.043477,
#     #             user_lng=39.668206,
#     #             dest_lat=-4.035606,
#     #             dest_lng=39.668558,
#     #             time="2024-11-26 15:00",
#     #             driver_id=2,
#     #             customer_id=2
#     #         )
#     #     ]
#     #     for order in orders:
#     #         db.session.add(order)

#     #     # Seed Rides
#     #     rides = [
#     #         Ride(
#     #             distance=12.5,
#     #             loader_cost=300,
#     #             from_location="Nairobi CBD",
#     #             to_location="Westlands",
#     #             price=2200,
#     #             order_id=1
#     #         ),
#     #         Ride(
#     #             distance=25.0,
#     #             loader_cost=450,
#     #             from_location="Mombasa Town",
#     #             to_location="Nyali",
#     #             price=4800,
#     #             order_id=2
#     #         )
#     #     ]
#     #     for ride in rides:
#     #         db.session.add(ride)

#     #     # Seed Ratings
#     #     ratings = [
#     #         Rating(rating_score=5, order_id=1, ride_id=1),
#     #         Rating(rating_score=4, order_id=2, ride_id=2)
#     #     ]
#     #     for rating in ratings:
#     #         db.session.add(rating)

#     #     # Commit all changes
#     #     db.session.commit()
#     #     print("Database seeded successfully!")

#     # # Run the seeding function
#     # if __name__ == "__main__":
#     #     seed_database()
