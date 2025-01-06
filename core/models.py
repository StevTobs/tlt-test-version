# core/models.py

from django.db import models

class Province(models.Model):
    id = models.IntegerField(primary_key=True)
    name_th = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    geography_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically set on update
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name_th

class Amphure(models.Model):
    id = models.IntegerField(primary_key=True)
    name_th = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    province = models.ForeignKey(Province, related_name='amphures', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically set on update
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name_th

class Tambon(models.Model):
    id = models.IntegerField(primary_key=True)
    zip_code = models.IntegerField()
    name_th = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    amphure = models.ForeignKey(Amphure, related_name='tambons', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    updated_at = models.DateTimeField(auto_now=True)      # Automatically set on update
    deleted_at = models.DateTimeField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)        # Latitude
    lng = models.FloatField(null=True, blank=True)        # Longitude

    def __str__(self):
        return self.name_th
