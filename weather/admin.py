from django.contrib import admin
from .models import WeatherData, KeralaCropCalendar, KeralaMarketPrice, PestDetection, CropRecommendation


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'temperature', 'humidity', 'rainfall', 'weather_condition', 'date']
    list_filter = ['location', 'date']
    search_fields = ['location', 'weather_condition']
    readonly_fields = ['date']
    ordering = ['-date']


@admin.register(KeralaCropCalendar)
class KeralaCropCalendarAdmin(admin.ModelAdmin):
    list_display = ['crop', 'season', 'kerala_district', 'planting_date', 'harvest_date']
    list_filter = ['season', 'kerala_district']
    search_fields = ['crop', 'kerala_district']
    ordering = ['season', 'planting_date']


@admin.register(KeralaMarketPrice)
class KeralaMarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'district', 'market_name', 'price_per_kg', 'trend', 'date']
    list_filter = ['crop', 'district', 'trend', 'date']
    search_fields = ['crop', 'district', 'market_name']
    ordering = ['-date']


@admin.register(PestDetection)
class PestDetectionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'detected_pest', 'confidence', 'severity', 'created_at']
    list_filter = ['severity', 'created_at']
    search_fields = ['detected_pest', 'treatment_recommendation']
    ordering = ['-created_at']


@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'season', 'success_probability', 'expected_yield', 'created_at']
    list_filter = ['season', 'created_at']
    search_fields = ['recommended_crops', 'fertilizer_suggestion']
    ordering = ['-created_at']
