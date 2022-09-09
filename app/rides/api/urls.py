from rest_framework.routers import DefaultRouter

from django.urls import path
from django.urls.conf import include

from rides.api.views import CarViewSet, RideViewSet, CityViewSet

router = DefaultRouter()
router.register('cars', CarViewSet, basename='cars')
router.register('rides', RideViewSet, basename='rides')
router.register('cities', CityViewSet, basename='cities')

urlpatterns = [
    path('', include(router.urls)),
]
