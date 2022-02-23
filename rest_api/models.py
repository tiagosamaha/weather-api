from django.db import models


class Weather(models.Model):
  date = models.DateField()
  lat = models.DecimalField(max_digits=6, decimal_places=4)
  lon = models.DecimalField(max_digits=7, decimal_places=4)
  city = models.CharField(max_length=255)
  state = models.CharField(max_length=255)
  temperatures = models.JSONField()
