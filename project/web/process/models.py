from django.db import models
# from django.contrib.postgres.fields import JSONField
from user.models import SolarPlant, User

class Zone(models.Model):
    zone_name = models.CharField(max_length=256)
    points = models.JSONField(default=list)

class Task(models.Model):
    status = models.BooleanField(default=False)
    collected_time = models.DateTimeField()
    submitted_time = models.DateTimeField(null=True, blank=True) # for in process AI
    upload_time = models.DateTimeField() # for upload file to process
    solarPlant = models.ForeignKey(SolarPlant, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    zones = models.ManyToManyField(Zone)

    WEATHER_CONDITIONS = (
    ("SUNNY", "Sunny"),
    ("WINDY", "Windy"),
    ("CLOUDY", "Cloudy"),
    ("RAINY", "Rainy"),
)

    weather = models.CharField(max_length=10, choices=WEATHER_CONDITIONS)
    temperature = models.FloatField(default=0)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)

