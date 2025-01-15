# client/data_models/utils.py

# from geopy.geocoders import Nominatim
# from geopy.extra.rate_limiter import RateLimiter
# from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import GoogleV3

import logging

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_lat_lon_geopy(province, amphoe, tambon):
    """
    Retrieves the latitude and longitude for a given province, amphoe, and tambon in Thailand.

    Parameters:
        province (str): The Thai name of the province.
        amphoe (str): The Thai name of the amphoe (district).
        tambon (str): The Thai name of the tambon (subdistrict).

    Returns:
        tuple: (latitude, longitude) if successful, else (None, None)
    """
    try:
        geolocator = Nominatim(user_agent="tltWebApp_geocoder")

        # Implement a rate limiter to respect Nominatim's usage policy
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)

        # Construct the full address
        address = f"{tambon}, {amphoe}, {province}, Thailand"

        # Geocode the address
        location = geocode(address)

        if location:
            logger.info(f"Successfully geocoded address '{address}' to lat: {location.latitude}, lon: {location.longitude}.")
            return (location.latitude, location.longitude)
        else:
            logger.warning(f"Geocoding failed: Location not found for address '{address}'.")
            return (None, None)

    except (GeocoderServiceError, GeocoderTimedOut) as e:
        logger.error(f"Geocoding error for address '{address}': {e}")
        return (None, None)
    except Exception as e:
        logger.error(f"Unexpected error for address '{address}': {e}")
        return (None, None)


def get_lat_lon_google(province, amphoe, tambon):
    geolocator = GoogleV3(api_key="AIzaSyAcxleJw_Ebq9t42a8vFsH7uziE3rzk-EY")
    address = f"{tambon}, {amphoe}, {province}, Thailand"
    
    try:
        location = geolocator.geocode(address)
        if location:
            return (location.latitude, location.longitude)
        else:
            return (None, None)
    except Exception as e:
        print(f"Error: {e}")
        return (None, None)
