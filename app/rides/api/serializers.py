"""
Ride Serializers
"""
from dataclasses import fields
from rest_framework import serializers

from rides.models import Car, Ride, Route, City, RegisteredRide

class CitySerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = City
        fields = ['id', 'name']

class RouteSerializer(serializers.ModelSerializer):
    """
    """
    to_city = serializers.StringRelatedField(read_only=True)
    from_city = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Route
        fields = ['to_city', 'from_city', 'rate']

class CarSerializer(serializers.ModelSerializer):
    """
    Model Serializer for car
    """
    class Meta:
        """
        Model Mata Class
        """
        model = Car
        fields = ['id', 'car', 'make_year', 'color', 'seating_capacity', 'registration_number']
        read_only_fields = ['id', 'owner']

class RideSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Ride
    """
    car_data = CarSerializer(read_only=True, source='car')
    route_data = RouteSerializer(read_only=True, source='route')

    class Meta:
        model = Ride
        fields = [
            'id', 'available_seats', 'booked_seats', 
            'gender', 'route', 'car', 'date', 'pickup_location', 'dropoff_location',
            'car_data', 'route_data',
        ]
        read_only_fields = ['id', 'user', 'status', 'car_data', 'route_data']

class RegisteredRideSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = RegisteredRide
        fields = ['id', 'instructions', 'number_of_riders', 'date', 'ride_id', 'user']
        read_only_fields = ['id', 'user']
