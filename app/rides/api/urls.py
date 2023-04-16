from rest_framework.routers import DefaultRouter
from push_notifications.api.rest_framework import GCMDeviceAuthorizedViewSet

from django.urls import path
from django.urls.conf import include

from rides.api.views import CarViewSet, RideViewSet, CityViewSet, RiderRideViewSet, RegisteredRideViewSet

router = DefaultRouter()
router.register('cars', CarViewSet, basename='cars')
router.register('rides', RideViewSet, basename='rides')
router.register('rider_rides', RiderRideViewSet, basename='rider_rides')
router.register('registered_rides', RegisteredRideViewSet, basename='register_rides')
router.register('cities', CityViewSet, basename='cities')
router.register('device/gcm', GCMDeviceAuthorizedViewSet, basename='apns_device')


urlpatterns = [
    path('', include(router.urls)),
    # path('device/gcm/', GCMDeviceAuthorizedViewSet, name='create_apns_device'),
]
