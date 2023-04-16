"""
Admin models
"""
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from rides.models import Ride, Route, RegisteredRide, Car, City, Location
from rides.resource import CityResource, RouteResource

class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource

class RouteAdmin(ImportExportModelAdmin):
    resource_class = RouteResource

admin.site.register(Ride)
admin.site.register(Route, RouteAdmin)
admin.site.register(RegisteredRide)
admin.site.register(Car)
admin.site.register(City, CityAdmin)
admin.site.register(Location)
