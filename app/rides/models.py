"""
this script contains all models definitions for our carpool application
"""
import jsonfield

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
APP_LABEL = 'rides'

class Car(models.Model):
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
        return "{}-{}".format(self.to_city, self.from_city)
    class Meta:
        app_label = APP_LABEL

class Ride(models.Model):
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
    pickup_locations = models.ManyToManyField('Location')
    dropoff_locations = models.ManyToManyField('Location')

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

    def __str__(self):
        return f"location for Ride {self.ride.pk}"

    class Meta:
        app_label = APP_LABEL

class RegisteredRide(models.Model):
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
    date = models.DateField()
    ride_id = models.ForeignKey(Ride, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup = models.CharField(max_length=200, null=True)
    dropoff = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=12, choices=StatusOptions, default='PENDING')

    class Meta:
        unique_together = ('user', 'ride_id')
        app_label = APP_LABEL
        verbose_name = "Registered Rides"
