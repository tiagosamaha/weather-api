from rest_framework import serializers

from .models import Weather


class WeatherSerializer(serializers.ModelSerializer):
    temperatures = serializers.ListField(child=serializers.FloatField())
    lat = serializers.DecimalField(max_digits=6, decimal_places=4, coerce_to_string=False)
    lon = serializers.DecimalField(max_digits=7, decimal_places=4, coerce_to_string=False)

    class Meta:
        model = Weather
        fields = '__all__'

    def validate_temperatures(self, value):
        if len(value) != 24:
            raise serializers.ValidationError('Define hourly temperatures')
        return value
