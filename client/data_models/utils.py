# client/data_models/utils.py

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
import logging

# Initialize logger
logger = logging.getLogger(__name__)

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
        # Initialize Nominatim Geocoder with a unique user agent
        geolocator = Nominatim(user_agent="tltWebApp_geocoder")

        # Implement a rate limiter to respect Nominatim's usage policy
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        # Construct the full address
        address = f"{tambon}, {amphoe}, {province}, Thailand"

        # Geocode the address
        location = geocode(address)

        if location:
            return (location.latitude, location.longitude)
        else:
            logger.warning(f"Geocoding failed: Location not found for address '{address}'.")
            return (None, None)

    except (GeocoderServiceError, GeocoderTimedOut) as e:
        logger.error(f"Geocoding error for address '{address}': {e}")
        return (None, None)
