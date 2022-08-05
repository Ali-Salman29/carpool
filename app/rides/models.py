"""
this script contains all models definitions for our carpool application
"""
import jsonfield
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Cars(models.Model):
    """
    models to save Users car information
    """
    car = models.CharField(max_length=200)
    make_year = models.IntegerField()
    color = models.CharField(max_length=50)
    seating_capacity = models.IntegerField()
    registration_number = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

class City(models.Model):
    """
    model to store cities
    """
    name = models.CharField(max_length=100)

class Route(models.Model):
    """
    model to store users travel information
    """
    id = models.IntegerField(primary_key=True)
    rate = models.IntegerField()
    to_city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='to_city')
    from_city = models.ForeignKey(City,on_delete=models.CASCADE,related_name='from_city')

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
    available_seats = models.IntegerField()
    booked_seats = models.IntegerField()
    status = models.CharField(max_length=10,choices=RideOptions,default='AVAILABLE')
    gender = models.CharField(max_length=10,choices=GenderOptions,default='NONE')
    route = models.ForeignKey(Route,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    car = models.ForeignKey(Cars,on_delete=models.CASCADE)
    date = models.DateField()
    pickup_location = jsonfield.JSONField(default={},blank=True)
    dropoff_location =jsonfield.JSONField(default={},blank=True)
    
class RegisteredRides(models.Model):
    """
    model to show rides history to client and significant info for service provider
    """
    instructions = models.CharField(max_length=500)
    number_of_riders = models.IntegerField()
    date = models.DateField()
    ride_id=models.ForeignKey(Ride,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        """
        added together relations of User and Rides model
        """
        unique_together = ('user', 'ride_id')
