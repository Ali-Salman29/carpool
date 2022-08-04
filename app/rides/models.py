"""
this script contains all models definitions for our carpool application
"""
from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Cars(models.Model):
    """
    models to save Users car information
    """
    car_model= models.CharField(max_length=200)
    make_year= models.IntegerField()
    color= models.CharField(max_length=50)
    seating_capacity= models.IntegerField()
    registration_number=models.CharField(primary_key=True)
    user_id=models.ForeignKey('User',on_delete=models.CASCADE)

class City(models.Model):
    """
    model to store cities
    """
    name=models.CharField()
    id=models.PositiveSmallIntegerField()

class Route(models.Model):
    """
    model to store users travel information
    """
    id= models.IntegerField()
    rate=models.IntegerField()
    to_city=models.ForeignKey('City',on_delete=models.CASCADE)
    from_city=models.ForeignKey('City',on_delete=models.CASCADE)

class Rides(models.Model):
    """
    model to show available rides to the user
    """
    ride_id=models.IntegerField(primary_key=True)
    available_seats=models.IntegerField()
    booked_seats =models.IntegerField()
    status=models.BooleanField()
    gender =models.CharField()
    route=models.ForeignKey('Route',on_delete=models.CASCADE)
    user_id=models.ForeignKey('User',on_delete=models.CASCADE)
    car_id=models.ForeignKey('Car',on_delete=models.CASCADE)
    date=models.DateField(auto_now=True)
    pickup_location=models.JSONField()
    dropoff_location=models.JSONField()

class RegisteredRides(models.Model):
    """
    model to show rides history to client and significant info for service provider
    """
    user_id=models.ForeignKey('User',unique=True,on_delete=models.CASCADE)
    ride_id=models.ForeignKey('Rides',unique=True,on_delete=models.CASCADE)
    Instructions=models.CharField(max_length=500)
    number_of_riders=models.IntegerField()
    date=models.DateField()

class Location(models.Model):
    """
    model to store users locations history and information
    """
    location_id=models.SlugField(primary_key=True)
    address=models.CharField()
    latitude=models.CharField()
    longitude=models.CharField()
    ride_id=models.ForeignKey('Rides',on_delete=models.CASCADE)
    