from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=500)
    phone_number = models.CharField(max_length=15)
    location = models.PointField(default='POINT(0 0)', srid=4326)
    date_created = models.DateTimeField(default=timezone.now)

    @property
    def longitude(self):
        return self.location[0]

    @property
    def latitude(self):
        return self.location[1]
