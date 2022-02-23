from django.urls import include, path

from rest_framework import routers

from rest_api.views import WeatherViewSet


router = routers.DefaultRouter()
router.register(r'weather', WeatherViewSet)


urlpatterns = [
    path('', include(router.urls))
]
