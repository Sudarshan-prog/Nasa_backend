
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    country = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    query_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ['latitude', 'longitude']

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"

class WeatherPrediction(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    target_date = models.DateField()
    predicted_temp_max = models.FloatField(null=True, blank=True)
    predicted_temp_min = models.FloatField(null=True, blank=True)
    predicted_precipitation = models.FloatField(null=True, blank=True)
    predicted_wind_speed = models.FloatField(null=True, blank=True)
    confidence_score = models.IntegerField(default=70)
    prediction_method = models.CharField(max_length=50, default='api_forecast')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather for {self.location.name} on {self.target_date}"
