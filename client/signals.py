# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from account.models import LocationData
from account.utils import get_lat_lon_geopy, get_lat_lon_google

@receiver(pre_save, sender=LocationData)
def populate_lat_lng(sender, instance, **kwargs):
    """
    Signal to auto-populate lat and lng before saving LocationData instance.
    """
    # Check if lat and lng are not set
    if not instance.lat or not instance.lng:
        try:
            latitude, longitude = get_lat_lon_google(
                province=instance.province,
                amphoe=instance.amphure,
                tambon=instance.tambon
            )
            instance.lat = latitude
            instance.lng = longitude
        except Exception as e:
            raise ValidationError(f"Error fetching coordinates: {e}")
