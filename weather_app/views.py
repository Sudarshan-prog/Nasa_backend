
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import date
import time

from .weather_service import WeatherService
from .models import Location, WeatherPrediction
from .serializers import WeatherPredictionRequestSerializer

@api_view(['POST'])
def predict_weather(request):
    """Main weather prediction endpoint"""

    serializer = WeatherPredictionRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({
            'error': 'Invalid request data',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data
    latitude = data['latitude']
    longitude = data['longitude']
    target_date = data['target_date']
    location_name = data.get('location_name', f"Location {latitude:.2f}, {longitude:.2f}")

    try:
        # Get or create location
        location, created = Location.objects.get_or_create(
            latitude=round(latitude, 4),
            longitude=round(longitude, 4),
            defaults={'name': location_name, 'query_count': 0}
        )
        location.query_count += 1
        location.save()

        # Generate prediction
        weather_service = WeatherService()
        prediction_result = weather_service.predict_weather(
            latitude, longitude, target_date, location_name
        )

        # Save prediction to database
        WeatherPrediction.objects.create(
            location=location,
            target_date=target_date,
            predicted_temp_max=prediction_result['weather_prediction']['temperature']['max_celsius'],
            predicted_temp_min=prediction_result['weather_prediction']['temperature']['min_celsius'],
            predicted_precipitation=prediction_result['weather_prediction']['precipitation']['amount_mm'],
            predicted_wind_speed=prediction_result['weather_prediction']['wind']['speed_kmh'],
            confidence_score=prediction_result['prediction_info']['confidence'],
            prediction_method=prediction_result['prediction_info']['method']
        )

        return Response(prediction_result)

    except Exception as e:
        return Response({
            'error': 'Weather prediction failed',
            'details': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_locations(request):
    """Get popular locations"""
    locations = Location.objects.filter(query_count__gt=0).order_by('-query_count')[:10]

    data = [{
        'id': loc.id,
        'name': loc.name,
        'latitude': loc.latitude,
        'longitude': loc.longitude,
        'query_count': loc.query_count
    } for loc in locations]

    return Response(data)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '1.0'
    })
