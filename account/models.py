from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from client.data_models.utils import get_lat_lon_geopy  # Import the utility function

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=135)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_investor = models.BooleanField(default=False, verbose_name="Are you an investor?")  # Add this field

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
def validate_lat(value):
    if not -90 <= value <= 90:
        raise ValidationError('Latitude must be between -90 and 90 degrees.')

def validate_lng(value):
    if not -180 <= value <= 180:
        raise ValidationError('Longitude must be between -180 and 180 degrees.')

class LocationData(models.Model):
    date = models.DateTimeField(primary_key=True, default=now, verbose_name="Date")  # Set date as primary key
    province = models.CharField(max_length=100, verbose_name="Province")
    amphure = models.CharField(max_length=100, verbose_name="Amphure")
    tambon = models.CharField(max_length=100, verbose_name="Tambon")
    # lat = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Latitude")
    # lng = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Longitude")
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="locations")
    lat = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="พิกัดละติจูด",
        validators=[validate_lat], blank=True, null=True
    )
    lng = models.DecimalField(
        max_digits=9, decimal_places=6, verbose_name="พิกัดลองจิจูด",
        validators=[validate_lng], blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="locations",
        verbose_name="User"
    )
    def __str__(self):
        return f"{self.province}, {self.amphure}, {self.tambon} on {self.date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Location Data"
        verbose_name_plural = "Location Data"
        ordering = ['-date']
        indexes = [
            models.Index(fields=['province', 'amphure', 'tambon']),
            models.Index(fields=['lat', 'lng']),
        ]

    def save(self, *args, **kwargs):
        """
        Override the save method to auto-populate lat and lng fields
        based on province, amphure, and tambon.
        """
        # Check if lat and lng are not already set or if location fields have changed
        if not self.lat or not self.lng:
            try:
                # Fetch latitude and longitude using the utility function
                latitude, longitude = get_lat_lon_geopy(
                    province=self.province,
                    amphoe=self.amphure,
                    tambon=self.tambon
                )
                self.lat = latitude
                self.lng = longitude
            except Exception as e:
                # Handle exceptions (e.g., log the error, set default values, etc.)
                # Here, we'll raise a ValidationError
                raise ValidationError(f"Error fetching coordinates: {e}")

        super(LocationData, self).save(*args, **kwargs)

class Visit(models.Model):
    location = models.ForeignKey(LocationData, related_name='visits', on_delete=models.CASCADE)
    visitor_id = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    time_spent = models.PositiveIntegerField(help_text="Time spent in minutes")

    def __str__(self):
        return f"Visit by {self.visitor_id} on {self.date}"