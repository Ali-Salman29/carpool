from posixpath import basename
from django.urls import path
from django.urls.conf import include
from rest_framework.routers import DefaultRouter
from rides.api.views import CarViewSet, RideViewSet

router = DefaultRouter()
router.register(r'cars', CarViewSet, basename='cars')
router.register(r'rides', RideViewSet, basename='rides')

urlpatterns = [
    path('', include(router.urls)),
]
