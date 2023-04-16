"""
Rides Views
"""
import json

from django.http import HttpResponse
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters

from rides.api.serializers import RideSerializer, CarSerializer, CitySerializer
from rides.models import Car, Ride, City, Location
from rides.api.permissions import IsOwnerOrAdmin
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

class RideFilter(filters.FilterSet):
    """
    A filter class to filter rides based on various criteria.
    """
    date = filters.DateFilter(field_name='date', lookup_expr='date')
    from_city = filters.NumberFilter(field_name='route__from_city')
    to_city = filters.NumberFilter(field_name='route__to_city')
    pickup_max_distance = filters.NumberFilter(method='filter_pickup_max_distance')
    dropoff_max_distance = filters.NumberFilter(method='filter_dropoff_max_distance')

    def filter_pickup_max_distance(self, queryset, name, value):
        """
        Filter rides near to pickup location
        """
        user_pickup_lat = self.data.get('user_pickup_lat')
        user_pickup_lon = self.data.get('user_pickup_lon')

        if user_pickup_lat and user_pickup_lon:
            pickup_point = Point(float(user_pickup_lon), float(user_pickup_lat))
            filtered_rides = Location.objects.filter(ride__in=queryset, location__distance_lte=(pickup_point, Distance(km=value)))
            return Ride.objects.filter(pk__in=filtered_rides.values_list('ride_id', flat=True))
        return queryset
    
    def filter_dropoff_max_distance(self, queryset, name, value):
        """
        Filter rides near to dropoff location
        """
        user_dropoff_lat = self.data.get('user_dropoff_lat')
        user_dropoff_lon = self.data.get('user_dropoff_lon')

        if user_dropoff_lat and user_dropoff_lon:
            dropoff_point = Point(float(user_dropoff_lon), float(user_dropoff_lat))
            filtered_rides = Location.objects.filter(ride__in=queryset, location__distance_lte=(dropoff_point, Distance(km=value)))
            return Ride.objects.filter(pk__in=filtered_rides.values_list('ride_id', flat=True))
        return queryset
    
    class Meta:
        """
        Metadata class for RideFilter
        """
        model = Ride
        fields = ['from_city', 'to_city', 'date']


class CarViewSet(viewsets.ModelViewSet):
    """
    Car Viewset
    """
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Return queryset filtered by owner
        """
        return Car.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        """
        Save user object before creating
        """
        serializer.save(owner=self.request.user)

class CityViewSet(viewsets.ModelViewSet):
    """
    Cities Viewset
    """
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]
    queryset = City.objects.all()

class RideViewSet(viewsets.ModelViewSet):
    """
    Ride Viewset
    """
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save user object before creating
        """
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        """
        Returns filterd rides based on query parms
        """
        
        queryset = Ride.objects.all()
        data = self.request.GET.dict()
        if 'pickup_max_distance' not in data:
            data['pickup_max_distance'] = 5
        if 'dropoff_max_distance' not in data:
            data['dropoff_max_distance'] = 5
        
        queryset = RideFilter(data, queryset=queryset).qs
        return queryset
    
    # def get_queryset(self):
    #     """
    #     Return filtered queryset
    #     """
    #     date = self.request.query_params.get('date', None)
    #     seats = self.request.query_params.get('seats', None)
    #     to_city = self.request.query_params.get('to_city', None)
    #     from_city = self.request.query_params.get('from_city', None)
    #     rides = Ride.objects.filter(status="AVAILABLE")
    #     # rides = Ride.objects.all()
    #     if date:
    #         rides = rides.filter(date__contains=date)
    #     if to_city:
    #         rides = rides.filter(route__to_city=to_city)
    #     if from_city:
    #         rides = rides.filter(route__from_city=from_city)
    #     if seats:
    #         rides = rides.filter(available_seats=seats)
    #     return rides
    
    @action(detail=False, methods=['get'])
    def get_all_cities(self, requset):
        """
        Get all cities
        """
        rides = self.get_queryset()
        city_ids = []
        if self.request.query_params.get('from_city', None):
            city_ids = rides.values_list('route__to_city', flat=True).distinct()
        else:
            city_ids = rides.values_list('route__from_city', flat=True).distinct()
        cities = City.objects.filter(id__in=city_ids)
        city_serializer = CitySerializer(cities, many=True)
        return HttpResponse(json.dumps(city_serializer.data), content_type='application/json')
    
    @action(detail=False, methods=['get'], url_path='get_available_cities/(?P<to_city>[^/.]+)')
    def get_available_cities(self, requset, to_city):
        """
        Get available cities
        """
        date = self.request.query_params.get('date', None)
        rides = Ride.objects.filter(status="AVAILABLE", route__to_city=to_city)
        if date:
            rides = rides.filter(date__contains=date)
        city_ids = rides.values_list('route__from_city', flat=True).distinct()
        cities = City.objects.filter(id__in=city_ids)
        city_serializer = CitySerializer(cities, many=True)
        return HttpResponse(json.dumps(city_serializer.data), content_type='application/json')

class RideAPIListView(generics.ListAPIView):
    """
    A view that returns a list of rides.

    This view supports the following query parameters:
        - from_city: Filters rides based on the starting city name.
        - to_city: Filters rides based on the destination city name.
        - date: Filters rides based on the departure date.

    If the following query parameters are present, the view applies additional geo filters:
        - user_pickup_lat: The latitude of the pickup location.
        - user_pickup_lon: The longitude of the pickup location.
        - user_dropoff_lat: The latitude of the dropoff location.
        - user_dropoff_lon: The longitude of the dropoff location.
    """
    serializer_class = RideSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Returns filterd rides based on query parms
        """
        
        queryset = Ride.objects.filter(status='AVAILABLE').exclude(user=self.request.user)
        data = self.request.GET.dict()
        if 'pickup_max_distance' not in data:
            data['pickup_max_distance'] = 5
        if 'dropoff_max_distance' not in data:
            data['dropoff_max_distance'] = 5
        
        queryset = RideFilter(data, queryset=queryset).qs
        return queryset

class RegisterRide(generics.ListAPIView):
    """
    Register Ride Viewset
    """
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return filtered queryset
        """
        queryset = Ride.objects.all()
        self.request.query_params.get('to')


