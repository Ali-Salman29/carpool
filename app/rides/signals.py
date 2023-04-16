import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from rides.models import RegisteredRide
from push_notifications.models import GCMDevice

@receiver(post_save, sender=RegisteredRide)
def send_notification_to_rider(sender, instance, created, **kwargs):
    """
    Send notification to the rider about ride 
    """
    if not created:
        return
    rider_device = GCMDevice.objects.get(user=instance.ride.user)
    message = {
        'type': 'new_ride_request',
        'ride_id': instance.ride.id,
        'pickup_location': instance.pickup.address,
        'dropoff_location': instance.dropoff.address,
        'username': instance.user.username
    }
    rider_device.send_message(json.dumps(message), collapse_key='new_ride_request')
