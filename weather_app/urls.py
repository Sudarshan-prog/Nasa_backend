
from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_weather, name='predict_weather'),
    path('locations/', views.get_locations, name='get_locations'),
    path('health/', views.health_check, name='health_check'),
]
