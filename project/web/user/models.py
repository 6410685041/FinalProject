from django.db import models
from django.contrib.auth.models import AbstractUser
from location_field.models.plain import PlainLocationField
import uuid

class SolarPlant(models.Model):
    solarPlant_name = models.CharField(max_length=256, null=False, blank=False)
    solarPlant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = PlainLocationField(null=False, blank=False)

class User(AbstractUser):
    occupations = (
        ("AD", "Admin"), 
        ("DO", "Drone Operator"),
        ("ST", "Solar Panel Technician"),
    )
    
    occupation = models.CharField(max_length=2, choices=occupations)
    email = models.EmailField(max_length=30, unique=True)
    solarPlant = models.ForeignKey(SolarPlant, on_delete=models.CASCADE)
