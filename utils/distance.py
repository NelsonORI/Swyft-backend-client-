import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth.
    
    Parameters:
        lat1, lon1: Latitude and longitude of the first point (in decimal degrees).
        lat2, lon2: Latitude and longitude of the second point (in decimal degrees).
    
    Returns:
        Distance in kilometers between the two points.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    radius_km = 6371  # Radius of Earth in kilometers
    return radius_km * c

#print(haversine(-1.2784631,36.751643, -1.328436,36.8806499))
#print(haversine(-1.2784631,36.751643, -1.2822722,36.7523652))