from django.contrib.gis import admin

from . models import *


class ProfilesAdmin(admin.OSMGeoAdmin):
    list_display = ['user', 'address', 'phone_number', 'location', 'date_created']
    search_fields = ['user', 'phone_number']


admin.site.register(Profile, ProfilesAdmin)
