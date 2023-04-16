"""
this script contains all models definitions for our carpool application
"""
import jsonfield

from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
APP_LABEL = 'rides'

class TimeStampedModel(models.Model):
    """
    TimeStampedModel

    An abstract base class model that provides self-managed "created" and
    "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         abstract = True

class Car(TimeStampedModel):
    """
    models to save Users car information
    """
    car = models.CharField(max_length=200)
    make_year = models.IntegerField()
    color = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    registration_number = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return "{}-{}".format(self.car, self.make_year)
    class Meta:
        app_label = APP_LABEL

class City(models.Model):
    """
    model to store cities
    """
    name = models.CharField(max_length=100)
    province = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
    class Meta:
        app_label = APP_LABEL
        verbose_name = "Cities"

class Route(models.Model):
    """
    model to store users travel information
    """
    rate = models.IntegerField()
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_city')
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city')

    def __str__(self):
        return f"{self.from_city}-{self.to_city}"
    class Meta:
        app_label = APP_LABEL

class Ride(TimeStampedModel):
    """
    model to show available rides to the user
    """
    RideOptions = [
        ('COMPLETED', 'Complete'),
        ('DELETED', 'Deleted'),
        ('AVAILABLE', 'Available'),
    ]
    GenderOptions = [('MALE','male'),('FEMALE','female'),('NONE','none')]
    available_seats = models.IntegerField(default=0)
    booked_seats = models.IntegerField(default=0)
    status = models.CharField(max_length=10, choices=RideOptions, default='AVAILABLE')
    gender = models.CharField(max_length=10, choices=GenderOptions, default='NONE')
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    date = models.DateTimeField()
    pickup_locations = models.ManyToManyField('Location', related_name='pickup_locations')
    dropoff_locations = models.ManyToManyField('Location', related_name='dropoff_locations')

    def __str__(self):
        return "{}-{}".format(str(self.route), self.date)

    class Meta:
        app_label = APP_LABEL

class Location(models.Model):
    """
    model to specify location with coordinates
    """
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    location = models.PointField()
    address = models.CharField(max_length=100)

    @property
    def location_coordinates(self):
        """
        Returns location coordinates
        """
        return {
            'latitude': self.location.y,
            'longitude': self.location.x
        }
    
    def __str__(self):
        return f"location for Ride {self.ride.pk}"

    class Meta:
        app_label = APP_LABEL

class RegisteredRide(TimeStampedModel):
    """
    model to show rides history to client and significant info for service provider
    """
    StatusOptions = [
        ('BOOKED', 'Booked'),
        ('PENDING', 'Pending'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]

    instructions = models.CharField(max_length=500)
    number_of_riders = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    pickup = models.ForeignKey(Location, null=True, on_delete=models.CASCADE, related_name='pickup')
    dropoff = models.ForeignKey(Location, null=True, on_delete=models.CASCADE, related_name='dropoff')
    status = models.CharField(max_length=12, choices=StatusOptions, default='PENDING')

    class Meta:
        unique_together = ('user', 'ride')
        app_label = APP_LABEL
        verbose_name = "Registered Rides"
