# locations/utils.py

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError

def get_lat_lon_geopy(province, amphoe, tambon):
    """
    Converts Thai administrative divisions to latitude and longitude using GeoPy's Nominatim.

    Parameters:
        province (str): Province name in Thai
        amphoe (str): Amphoe name in Thai
        tambon (str): Tambon name in Thai

    Returns:
        tuple: (latitude, longitude) if found, else (None, None)
    """
    geolocator = Nominatim(user_agent="location_converter")

    query = f"{tambon}, {amphoe}, {province}, Thailand"

    try:
        location = geolocator.geocode(query, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderServiceError:
        return None, None
