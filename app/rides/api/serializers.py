"""
Ride Serializers
"""
from rest_framework import serializers

from rides.models import Car, Ride, Route, City, RegisteredRide, Location
from django.contrib.gis.geos import Point

class CarSerializer(serializers.ModelSerializer):
    """
    The Serializer Serializes the Car Object
    """
    class Meta:
        """
        Meta Class
        """
        model = Car
        fields = '__all__'
        read_only_fields = ['id', 'owner']


class CitySerializer(serializers.ModelSerializer):
    """
    The Serializer Serializes the City Object 
    """
    class Meta:
        """
        Meta Class
        """
        model = City
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    """
    The Serializer Serializes the Route Object
    """
    to_city = CitySerializer()
    from_city = CitySerializer()

    class Meta:
        model = Route
        fields = '__all__'


class PointSerializer(serializers.Serializer):
    """
    Serializer for a geographic point using Django's PointField.
    """
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

    def to_representation(self, value):
        """
        Convert the Point object to a dictionary with longitude and latitude coordinates.
        """
        if isinstance(value, Point):
            return {'longitude': value.x, 'latitude': value.y}
        return None

    def to_internal_value(self, data):
        """
        Convert the dictionary with x and y coordinates to a Point object.
        """
        try:
            longitude = float(data['longitude'])
            latitude = float(data['latitude'])
            return Point(longitude, latitude)
        except (TypeError, KeyError, ValueError):
            raise serializers.ValidationError("Invalid point coordinates")


class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for a Location Object
    """
    location = PointSerializer()

    class Meta:
        """
        Meta Class
        """
        model = Location
        fields = ['id', 'address', 'location']


class RideSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ride Object
    """
    pickup_locations = LocationSerializer(many=True, required=True)
    dropoff_locations = LocationSerializer(many=True, required=True)
    to_city = serializers.IntegerField(required=True, write_only=True)
    from_city = serializers.IntegerField(required=True, write_only=True)
    car_id = serializers.IntegerField(required=True, write_only=True)
    car = CarSerializer(read_only=True)
    route = RouteSerializer(read_only=True)

    class Meta:
        """
        Meta Class
        """
        model = Ride
        fields = '__all__'
        read_only_fields = [
            'id', 'user', 'booked_seats', 'status', 'route',
        ]

    def create(self, validated_data):
        """
        Creates a ride from the validated data

        Args:
            validated_data (dict): serializable data

        Returns:
            Ride: Newly created ride
        """
        pickup_locations_data = validated_data.pop('pickup_locations', [])
        dropoff_locations_data = validated_data.pop('dropoff_locations', [])

        from_city = validated_data.pop('from_city', None)
        to_city = validated_data.pop('to_city', None)
        car_id = validated_data.pop('car_id', None)

        try:
            route = Route.objects.get(from_city=from_city, to_city=to_city)
        except Route.DoesNotExist as exc:
            raise serializers.ValidationError(
                f"route from {from_city} to {to_city} doesn't exsist") from exc

        car = Car.objects.get(id=car_id)
        ride = Ride.objects.create(route=route, car=car, **validated_data)

        pickup_locations = []
        for pickup_location_data in pickup_locations_data:
            location = Location.objects.create(
                ride=ride, **pickup_location_data)
            pickup_locations.append(location)

        dropoff_location = []
        for dropoff_location_data in dropoff_locations_data:
            location = Location.objects.create(
                ride=ride, **dropoff_location_data)
            dropoff_location.append(location)

        ride.pickup_locations.set(pickup_locations)
        ride.dropoff_locations.set(dropoff_location)

        return ride

    def update(self, instance, validated_data):
        """
        TODO: Update this function
        """
        pickup_locations_data = validated_data.pop('pickup_locations', [])
        dropoff_locations_data = validated_data.pop('dropoff_locations', [])

        car_id = validated_data.pop('car_id', None)
        car = Car.objects.get(id=car_id)
        instance.car = car
        instance.save()

        Location.objects.filter(ride=instance).delete()

        for pickup_location_data in pickup_locations_data:
            Location.objects.create(ride=instance, **pickup_location_data)

        for dropoff_location_data in dropoff_locations_data:
            Location.objects.create(ride=instance, **dropoff_location_data)

        return instance

class RegisteredRideSerializer(serializers.ModelSerializer):
    """
    The Serializer Serializes the Ride Object
    """
    class Meta:
        """
        Meta Class
        """
        model = RegisteredRide
        fields = "__all__"
        read_only_fields = ['id', 'user']
    
    def validate(self, data):
        """
        Validate fields
        """
        data = super(RegisteredRideSerializer, self).validate(data)

        ride = Ride.objects.prefetch_related('pickup_locations', 'dropoff_locations').get(id=data['ride'].id)
        if not ride.pickup_locations.filter(id=data['pickup'].id).exists():
            raise serializers.ValidationError("Invalide pickup location")
        
        if not ride.dropoff_locations.filter(id=data['dropoff'].id).exists():
            raise serializers.ValidationError("Invalide dropoff location")
    
        return data
