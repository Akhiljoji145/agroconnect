from django.urls import path
from . import views

app_name = "weather"

urlpatterns = [
    path("", views.weather_dashboard, name="dashboard"),
    path("crop-calendar/", views.crop_calendar, name="crop_calendar"),
    path("market-prices/", views.market_prices, name="market_prices"),
    path("pest-detection/", views.pest_detection, name="pest_detection"),
    path("recommendations/", views.get_crop_recommendation, name="recommendations"),
    path("fetch-weather/", views.fetch_weather_data, name="fetch_weather"),
    path("api/weather/", views.weather_api, name="weather_api"),
]
