from django.urls import include, path

from rest_framework import routers

from rest_api.views import WeatherViewSet


router = routers.DefaultRouter()
router.register(r'weathers', WeatherViewSet)


urlpatterns = [
    path('', include(router.urls))
]
