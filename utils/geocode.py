from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def geocode(address):
    geolocator = Nominatim(user_agent="swyft_kenya")
    try:
        location =geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except GeocoderTimedOut:
        return None

address = "Imara Daima"
coordinates = geocode(address)
print(coordinates)