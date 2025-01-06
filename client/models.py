from django.db import models
from account.models import CustomUser

# class ClientReport(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     province = models.CharField(max_length=100)
#     amphure = models.CharField(max_length=100, null=True, blank=True)
#     tambon = models.CharField(max_length=100, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Report for {self.user.username} - {self.province}"


class ClientLocInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.FloatField(verbose_name="Latitude")
    longitude = models.FloatField(verbose_name="Longitude")
    size_charger = models.CharField(max_length=100)
    num_charger = models.IntegerField()
    budget = models.FloatField()
    POI = models.CharField(max_length=100)  # Place of Interest
    ROI = models.FloatField()  # Return on Investment

    is_premium = models.BooleanField(default=False, verbose_name="Is this a premium location?")

    user = models.ForeignKey(CustomUser, max_length=10, on_delete=models.CASCADE, null=True)


