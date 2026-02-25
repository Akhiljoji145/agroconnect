from django.db import models
from django.contrib.auth.models import User


class WeatherData(models.Model):
    """Store weather information for Kerala districts"""
    location = models.CharField(max_length=100, help_text="Kerala district name")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperature in Celsius")
    humidity = models.DecimalField(max_digits=5, decimal_places=2, help_text="Humidity percentage")
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, help_text="Rainfall in mm")
    weather_condition = models.CharField(max_length=50, help_text="Current weather condition")
    forecast = models.TextField(help_text="Weather forecast for next 24 hours")
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Wind speed in km/h")
    pressure = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, help_text="Atmospheric pressure in hPa")
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Weather Data"
        verbose_name_plural = "Weather Data"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.location} - {self.date.strftime('%Y-%m-%d')}"


class KeralaCropCalendar(models.Model):
    """Kerala-specific crop planting calendar"""
    SEASON_CHOICES = [
        ('summer', 'Summer (Feb-May)'),
        ('monsoon', 'Monsoon (Jun-Sep)'),
        ('winter', 'Winter (Oct-Jan)'),
    ]
    
    farmer = models.ForeignKey('farmer.FarmerProfile', on_delete=models.CASCADE, null=True, blank=True)
    crop = models.CharField(max_length=100, help_text="Crop name")
    planting_date = models.DateField(help_text="Recommended planting date")
    harvest_date = models.DateField(help_text="Expected harvest date")
    season = models.CharField(max_length=20, choices=SEASON_CHOICES, help_text="Growing season")
    kerala_district = models.CharField(max_length=50, help_text="Kerala district")
    soil_type = models.CharField(max_length=50, help_text="Soil type recommendation")
    water_requirement = models.CharField(max_length=100, help_text="Water requirement details")
    fertilizer_recommendation = models.TextField(help_text="Fertilizer recommendations")
    pest_control_tips = models.TextField(help_text="Pest control recommendations")
    
    class Meta:
        verbose_name = "Crop Calendar"
        verbose_name_plural = "Crop Calendars"
        ordering = ['season', 'planting_date']
    
    def __str__(self):
        return f"{self.crop} - {self.get_season_display()}"


class KeralaMarketPrice(models.Model):
    """Kerala agricultural market prices"""
    TREND_CHOICES = [
        ('rising', 'Rising'),
        ('falling', 'Falling'),
        ('stable', 'Stable'),
    ]
    
    crop = models.CharField(max_length=50, help_text="Crop name")
    district = models.CharField(max_length=50, help_text="Kerala district")
    market_name = models.CharField(max_length=100, help_text="Market name")
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2, help_text="Price per kg in rupees")
    date = models.DateField(help_text="Price date")
    trend = models.CharField(max_length=20, choices=TREND_CHOICES, help_text="Price trend")
    market_notes = models.TextField(blank=True, help_text="Market conditions and notes")
    source = models.CharField(max_length=100, default="Kerala Agricultural Department", help_text="Data source")
    
    class Meta:
        verbose_name = "Market Price"
        verbose_name_plural = "Market Prices"
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.crop} - {self.district} - ₹{self.price_per_kg}"


class PestDetection(models.Model):
    """Pest detection and treatment recommendations"""
    farmer = models.ForeignKey('farmer.FarmerProfile', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="pest_images/", help_text="Upload pest/disease image")
    detected_pest = models.CharField(max_length=100, help_text="Detected pest or disease")
    confidence = models.DecimalField(max_digits=3, decimal_places=2, help_text="Detection confidence percentage")
    treatment_recommendation = models.TextField(help_text="Recommended treatment")
    severity = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], help_text="Severity level")
    affected_area = models.DecimalField(max_digits=8, decimal_places=2, help_text="Affected area in acres")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Pest Detection"
        verbose_name_plural = "Pest Detections"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.detected_pest} - {self.confidence}% confidence"


class CropRecommendation(models.Model):
    """AI-powered crop recommendations"""
    farmer = models.ForeignKey('farmer.FarmerProfile', on_delete=models.CASCADE, null=True, blank=True)
    soil_ph = models.DecimalField(max_digits=4, decimal_places=2, help_text="Soil pH level")
    moisture_level = models.DecimalField(max_digits=5, decimal_places=2, help_text="Soil moisture percentage")
    season = models.CharField(max_length=20, choices=KeralaCropCalendar.SEASON_CHOICES)
    recommended_crops = models.TextField(help_text="Recommended crops (comma separated)")
    success_probability = models.DecimalField(max_digits=3, decimal_places=2, help_text="Success probability percentage")
    expected_yield = models.DecimalField(max_digits=8, decimal_places=2, help_text="Expected yield in kg per acre")
    fertilizer_suggestion = models.TextField(help_text="Fertilizer suggestions")
    irrigation_needs = models.TextField(help_text="Irrigation requirements")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Crop Recommendation"
        verbose_name_plural = "Crop Recommendations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Recommendation for {self.season}"
