"""
Rides Resources
"""
from import_export import resources 

from rides.models import City, Route

class CityResource(resources.ModelResource):
     class Meta:
         model = City

class RouteResource(resources.ModelResource):
     class Meta:
         model = Route
