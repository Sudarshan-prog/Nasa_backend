
from django.contrib import admin
from .models import Location, WeatherPrediction

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'query_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    readonly_fields = ['created_at']

@admin.register(WeatherPrediction)
class WeatherPredictionAdmin(admin.ModelAdmin):
    list_display = ['location', 'target_date', 'prediction_method', 'confidence_score', 'created_at']
    list_filter = ['prediction_method', 'target_date', 'created_at']
    readonly_fields = ['created_at']
    date_hierarchy = 'target_date'
