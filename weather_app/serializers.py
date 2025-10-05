
from rest_framework import serializers
from datetime import date

class WeatherPredictionRequestSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90, max_value=90)
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    target_date = serializers.DateField()
    location_name = serializers.CharField(max_length=200, required=False)

    def validate_target_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Target date cannot be in the past")
        return value
