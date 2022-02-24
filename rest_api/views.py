from django.db.models import Q
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import BasePermission

from .models import Weather
from .serializers import WeatherSerializer


class WeatherFilter(FilterSet):
    city = CharFilter(method='cities_with_comma')

    class Meta:
        model = Weather
        exclude = ['temperatures']
    
    def cities_with_comma(self, queryset, name, value):
        query = Q()
        for city in value.split(","):
            query |= Q(city__icontains=city)
        return queryset.filter(query)


class CannotUpdate(BasePermission):
    def has_permission(self, request, view):
        return request.method in ['GET', 'POST', 'DELETE', 'OPTIONS', 'HEAD']


class WeatherViewSet(viewsets.ModelViewSet):
    queryset = Weather.objects.all()
    serializer_class = WeatherSerializer
    permission_classes = [CannotUpdate]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = WeatherFilter
    filterset_fields = ['city', 'date']
    ordering_fields = ['date']
