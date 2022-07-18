from PIL import Image
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils import timezone
from location_field.models.spatial import LocationField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=15)
    # location = models.PointField(default='POINT(0 0)', srid=4326)
    location = LocationField(zoom=7, default=Point(1.0, 1.0))
    date_created = models.DateTimeField(default=timezone.now)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def longitude(self):
        return self.location[0]

    @property
    def latitude(self):
        return self.location[1]
