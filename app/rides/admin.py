"""
Admin models
"""
from django.contrib import admin
from .models import (
    Ride, Route, RegisteredRide, Car, City
)

admin.site.register(Ride)
admin.site.register(Route)
admin.site.register(RegisteredRide)
admin.site.register(Car)
admin.site.register(City)
