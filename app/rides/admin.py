from django.contrib import admin
from .models import Ride
from .models import Route
from .models import RegisteredRides
from .models import Cars
from .models import User
from .models import City
# Register your models here.
admin.site.register(Ride)
admin.site.register(Route)
admin.site.register(RegisteredRides)
admin.site.register(Cars)
admin.site.register(City)
