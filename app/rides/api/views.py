"""
Rides Views
"""
import json

from django.http import HttpResponse
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from rides.api.serializers import RideSerializer, CarSerializer, CitySerializer
from rides.models import Car, Ride, City
from rides.api.permissions import IsOwnerOrAdmin


class CarViewSet(viewsets.ModelViewSet):
    """
    Car Viewset
    """
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        """
        pre_save userobject on create
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
        pre_save userobject on create
        """
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        date = self.request.query_params.get('date', None)
        seats = self.request.query_params.get('seats', None)
        to_city = self.request.query_params.get('to_city', None)
        from_city = self.request.query_params.get('from_city', None)
        # rides = Ride.objects.filter(status="AVAILABLE")
        rides = Ride.objects.all()
        if date:
            rides = rides.filter(date__contains=date)
        if to_city:
            rides = rides.filter(route__to_city=to_city)
        if from_city:
            rides = rides.filter(route__from_city=from_city)
        if seats:
            rides = rides.filter(available_seats=seats)
        return rides
    
    @action(detail=False, methods=['get'])
    def get_all_cities(self, requset):
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
        date = self.request.query_params.get('date', None)
        rides = Ride.objects.filter(status="AVAILABLE", route__to_city=to_city)
        if date:
            rides = rides.filter(date__contains=date)
        city_ids = rides.values_list('route__from_city', flat=True).distinct()
        cities = City.objects.filter(id__in=city_ids)
        city_serializer = CitySerializer(cities, many=True)
        return HttpResponse(json.dumps(city_serializer.data), content_type='application/json')

class RegisterRide(generics.ListAPIView):
    """
    Register Ride Viewset
    """
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Ride.objects.all()
        self.request.query_params.get('to')
