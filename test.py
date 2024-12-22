import jwt 

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNDE2NDE3NywianRpIjoiNmVkNDgwMjMtNGU2Yy00OWYwLTljMmYtMzBiZTc1ZjA0NDYzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImRyMDY0MiIsIm5iZiI6MTczNDE2NDE3NywiY3NyZiI6IjhmMzk2NGI0LTg0NGEtNGZjNi04MWNlLTkwYzE2NDExNDZlYSIsImV4cCI6MTczNDE2NTk3N30.VcTJSxYiImW_HbLrbCF81PhTK6YcuyThXAZWDLE2VpM'
secret_key = "jAMESwent_to_theparkandsawaracoon"

try:
    decode = jwt.decode(token, secret_key, algorithms=["HS256"])
    print(decode)

except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")


        