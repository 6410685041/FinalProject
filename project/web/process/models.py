from django.db import models
# from django.contrib.postgres.fields import JSONField
from user.models import SolarPlant, User

class Zone(models.Model):
    zone_name = models.CharField(max_length=256)
    points = models.JSONField(default=list)

class Task(models.Model):
    status = models.BooleanField(default=False)
    collected_time = models.TimeField()
    submitted_time = models.TimeField()
    solarPlant = models.ForeignKey(SolarPlant, on_delete=models.CASCADE)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    zones = models.ManyToManyField(Zone)

    WEATHER_CONDITIONS = (
    ("SUNNY", "Sunny"),
    ("WINDY", "Windy"),
    ("CLOUDY", "Cloudy"),
    ("RAINY", "Rainy"),
)

    weather = models.CharField(max_length=10, choices=WEATHER_CONDITIONS)
    file = models.FileField()
    video = models.FileField(upload_to='videos/')

