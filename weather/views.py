from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.utils import timezone
import requests
import json
from datetime import datetime, timedelta

from .models import WeatherData, KeralaCropCalendar, KeralaMarketPrice, PestDetection, CropRecommendation
from .forms import WeatherDataForm, KeralaCropCalendarForm, KeralaMarketPriceForm, PestDetectionForm, CropRecommendationForm


def weather_dashboard(request):
    """Main weather dashboard for Kerala"""
    weather_data = WeatherData.objects.all().order_by('-date')[:10]
    latest_weather = WeatherData.objects.all().order_by('-date').first()
    
    context = {
        'weather_data': weather_data,
        'latest_weather': latest_weather,
        'kerala_districts': [
            'Thiruvananthapuram', 'Kollam', 'Kochi', 'Thrissur',
            'Palakkad', 'Malappuram', 'Kozhikode', 'Wayanad',
            'Kannur', 'Kasaragod', 'Idukki', 'Ernakulam',
            'Alappuzha', 'Pathanamthitta'
        ]
    }
    return render(request, 'weather/dashboard.html', context)


def get_weather_api(district):
    """Get weather data from OpenWeatherMap API"""
    try:
        api_key = "your_openweather_api_key"  # Replace with actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={district},IN&appid={api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'weather_condition': data['weather'][0]['description'],
                'wind_speed': data.get('wind', {}).get('speed', 0),
                'pressure': data['main']['pressure'],
                'forecast': f"Expected conditions: {data['weather'][0]['description']}"
            }
    except Exception as e:
        print(f"Weather API error: {e}")
        return None


def fetch_weather_data(request):
    """Fetch weather data for Kerala districts"""
    district = request.GET.get('district', 'Kochi')
    weather_info = get_weather_api(district)
    
    if weather_info:
        # Save to database
        WeatherData.objects.create(
            location=district,
            temperature=weather_info['temperature'],
            humidity=weather_info['humidity'],
            rainfall=0,  # Would need separate API for rainfall
            weather_condition=weather_info['weather_condition'],
            forecast=weather_info['forecast'],
            wind_speed=weather_info['wind_speed'],
            pressure=weather_info['pressure']
        )
        messages.success(request, f"Weather data updated for {district}")
    else:
        messages.error(request, "Failed to fetch weather data")
    
    return redirect('weather:dashboard')


def crop_calendar(request):
    """Kerala crop calendar"""
    if request.method == 'POST':
        form = KeralaCropCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Crop calendar entry added successfully")
            return redirect('weather:crop_calendar')
    else:
        form = KeralaCropCalendarForm()
    
    calendar_data = KeralaCropCalendar.objects.all().order_by('season', 'planting_date')
    
    context = {
        'form': form,
        'calendar_data': calendar_data,
        'season_choices': KeralaCropCalendar.SEASON_CHOICES
    }
    return render(request, 'weather/crop_calendar.html', context)


def market_prices(request):
    """Kerala market prices"""
    if request.method == 'POST':
        form = KeralaMarketPriceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Market price data added successfully")
            return redirect('weather:market_prices')
    else:
        form = KeralaMarketPriceForm()
    
    market_data = KeralaMarketPrice.objects.all().order_by('-date')[:20]
    
    context = {
        'form': form,
        'market_data': market_data,
        'trend_choices': KeralaMarketPrice.TREND_CHOICES
    }
    return render(request, 'weather/market_prices.html', context)


@login_required
def pest_detection(request):
    """Pest detection and analysis"""
    if request.method == 'POST':
        form = PestDetectionForm(request.POST, request.FILES)
        if form.is_valid():
            pest_detection = form.save(commit=False)
            pest_detection.farmer = request.user.farmer_profile
            pest_detection.save()
            messages.success(request, "Pest detection analysis completed")
            return redirect('weather:pest_detection')
    else:
        form = PestDetectionForm()
    
    pest_data = PestDetection.objects.filter(farmer=request.user.farmer_profile).order_by('-created_at')[:10]
    
    context = {
        'form': form,
        'pest_data': pest_data
    }
    return render(request, 'weather/pest_detection.html', context)


def get_crop_recommendation(request):
    """AI-powered crop recommendations"""
    if request.method == 'POST':
        form = CropRecommendationForm(request.POST)
        if form.is_valid():
            recommendation = form.save(commit=False)
            recommendation.farmer = request.user.farmer_profile
            recommendation.save()
            messages.success(request, "Crop recommendation generated")
            return redirect('weather:recommendations')
    else:
        form = CropRecommendationForm()
    
    recommendations = CropRecommendation.objects.filter(farmer=request.user.farmer_profile).order_by('-created_at')[:5]
    
    context = {
        'form': form,
        'recommendations': recommendations
    }
    return render(request, 'weather/recommendations.html', context)


def simple_ai_recommendation(soil_ph, moisture, season):
    """Simple AI recommendation engine"""
    recommendations = {
        'summer': {
            'crops': ['Rice', 'Maize', 'Cotton', 'Sugarcane'],
            'success_rate': 85,
            'fertilizer': 'Urea and DAP recommended',
            'irrigation': 'Regular watering required'
        },
        'monsoon': {
            'crops': ['Paddy', 'Tapioca', 'Banana', 'Coconut'],
            'success_rate': 90,
            'fertilizer': 'Organic compost recommended',
            'irrigation': 'Natural rainfall sufficient'
        },
        'winter': {
            'crops': ['Wheat', 'Barley', 'Mustard', 'Potato'],
            'success_rate': 80,
            'fertilizer': 'NPK balanced fertilizer',
            'irrigation': 'Moderate watering needed'
        }
    }
    
    return recommendations.get(season, recommendations['summer'])


def weather_api(request):
    """API endpoint for weather data"""
    district = request.GET.get('district', 'Kochi')
    weather_info = get_weather_api(district)
    
    if weather_info:
        return JsonResponse({
            'status': 'success',
            'data': weather_info
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Weather data not available'
        })
