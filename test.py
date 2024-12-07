# import jwt 

# token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMzQyNzYzMiwianRpIjoiOWE2ZTU5NTEtYmU4Ni00YTYzLThlNTYtMGFiZWQ4Yzk4ZDRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRyMDY0MiIsIm5iZiI6MTczMzQyNzYzMiwiY3NyZiI6IjFkMWJlOGIxLTY3MGItNDFiYS1iYzMyLWU1MTRkYmQwNTdjOCIsImV4cCI6MTczMzQyODUzMn0.GQ1G3YnkvncsS2ISpNDTc7jBGumguvVQI-RBwQkx0BI'
# secret_key = "jAMESwent_to_theparkandsawaracoon"

# try:
#     decode = jwt.decode(token, secret_key, algorithms=["HS256"])
#     print(decode)

# except jwt.ExpiredSignatureError:
#     print("Token has expired")
# except jwt.InvalidTokenError:
#     print("Invalid token")

from models import Customer, Driver
from config import app

with app.app_context():
    drivers = Driver.query.all()

    for driver in drivers:
        print(driver.id)
        