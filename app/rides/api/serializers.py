"""
Ride Serializers
"""
from dataclasses import fields
import json
from xml.dom import ValidationErr
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
    to_city = CitySerializer(read_only=True)
    from_city = CitySerializer(read_only=True)

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

class LocationSerializer(serializers.Serializer):
    """
    """
    address = serializers.CharField(required=True)
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitute = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)

class RideSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Ride
    """
    car_data = CarSerializer(read_only=True, source='car')
    route_data = RouteSerializer(read_only=True, source='route')
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    pickup_location = LocationSerializer(many=True)
    dropoff_location = LocationSerializer(many=True)
    to_city = serializers.IntegerField(required=True, write_only=True)
    from_city = serializers.IntegerField(required=True, write_only=True)

    def create(self, validated_data):
        """
        """
        from_city = validated_data.pop('from_city', None)
        to_city = validated_data.pop('to_city', None)
        if not (to_city and from_city):
            raise serializers.ValidationError('to_city and from_city are required')
        try:
            route = Route.objects.get(to_city=to_city, from_city=from_city)
        except Route.DoesNotExist:
            raise serializers.ValidationError(f"route from {from_city} to {to_city} doesn't exsist")
        
        validated_data['route'] = route
        ride = Ride.objects.create(**validated_data)
        return ride

    def update(self, instance, validated_data):
        """
        """
        from_city = validated_data.pop('from_city', None)
        to_city = validated_data.pop('to_city', None)
        if not (to_city and from_city):
            raise serializers.ValidationError('to_city and from_city are required')
        try:
            route = Route.objects.get(to_city=to_city, from_city=from_city)
        except Route.DoesNotExist:
            raise serializers.ValidationError(f"route from {from_city} to {to_city} doesn't exsist")
        validated_data['route'] = route

        return super(RideSerializer, self).update(instance, validated_data)
    
    def to_representation(self, value):
        """
        Returns content of a version, data will remain in json format
        """
        if not isinstance(value.pickup_location, list): 
            value.pickup_location = json.loads(value.pickup_location)
            value.dropoff_location = json.loads(value.dropoff_location)
        return super(RideSerializer, self).to_representation(value)
    
    class Meta:
        model = Ride
        fields = [
            'id', 'available_seats', 'booked_seats', 
            'gender', 'route', 'car', 'date', 'pickup_location', 'dropoff_location',
            'car_data', 'route_data', 'to_city', 'from_city',
        ]
        read_only_fields = [
            'id', 'user', 'booked_seats', 'status', 'car_data',
            'route_data', 'route',
        ]

class RegisteredRideSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = RegisteredRide
        fields = ['id', 'instructions', 'number_of_riders', 'date', 'ride_id', 'user']
        read_only_fields = ['id', 'user']
