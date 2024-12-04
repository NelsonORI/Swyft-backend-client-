from config import app, db
from models import Driver, Customer

customers = Customer.query.all()
print(customers)
