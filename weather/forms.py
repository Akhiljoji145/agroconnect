from django import forms
from .models import WeatherData, KeralaCropCalendar, KeralaMarketPrice, PestDetection, CropRecommendation


class WeatherDataForm(forms.ModelForm):
    class Meta:
        model = WeatherData
        fields = ['location', 'temperature', 'humidity', 'rainfall', 'weather_condition', 
                  'forecast', 'wind_speed', 'pressure']
        widgets = {
            'location': forms.Select(choices=[
                ('Thiruvananthapuram', 'Thiruvananthapuram'),
                ('Kollam', 'Kollam'),
                ('Kochi', 'Kochi'),
                ('Thrissur', 'Thrissur'),
                ('Palakkad', 'Palakkad'),
                ('Malappuram', 'Malappuram'),
                ('Kozhikode', 'Kozhikode'),
                ('Wayanad', 'Wayanad'),
                ('Kannur', 'Kannur'),
                ('Kasaragod', 'Kasaragod'),
                ('Idukki', 'Idukki'),
                ('Ernakulam', 'Ernakulam'),
                ('Alappuzha', 'Alappuzha'),
                ('Pathanamthitta', 'Pathanamthitta'),
            ], attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'humidity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'rainfall': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'weather_condition': forms.TextInput(attrs={'class': 'form-control'}),
            'forecast': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'wind_speed': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'required': False}),
            'pressure': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'required': False}),
        }


class KeralaCropCalendarForm(forms.ModelForm):
    class Meta:
        model = KeralaCropCalendar
        fields = ['crop', 'planting_date', 'harvest_date', 'season', 'kerala_district', 
                  'soil_type', 'water_requirement', 'fertilizer_recommendation', 'pest_control_tips']
        widgets = {
            'crop': forms.TextInput(attrs={'class': 'form-control'}),
            'planting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'harvest_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'season': forms.Select(attrs={'class': 'form-control'}),
            'kerala_district': forms.Select(choices=[
                ('Thiruvananthapuram', 'Thiruvananthapuram'),
                ('Kollam', 'Kollam'),
                ('Kochi', 'Kochi'),
                ('Thrissur', 'Thrissur'),
                ('Palakkad', 'Palakkad'),
                ('Malappuram', 'Malappuram'),
                ('Kozhikode', 'Kozhikode'),
                ('Wayanad', 'Wayanad'),
                ('Kannur', 'Kannur'),
                ('Kasaragod', 'Kasaragod'),
                ('Idukki', 'Idukki'),
                ('Ernakulam', 'Ernakulam'),
                ('Alappuzha', 'Alappuzha'),
                ('Pathanamthitta', 'Pathanamthitta'),
            ], attrs={'class': 'form-control'}),
            'soil_type': forms.TextInput(attrs={'class': 'form-control'}),
            'water_requirement': forms.TextInput(attrs={'class': 'form-control'}),
            'fertilizer_recommendation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pest_control_tips': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class KeralaMarketPriceForm(forms.ModelForm):
    class Meta:
        model = KeralaMarketPrice
        fields = ['crop', 'district', 'market_name', 'price_per_kg', 'date', 'trend', 'market_notes']
        widgets = {
            'crop': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.Select(choices=[
                ('Thiruvananthapuram', 'Thiruvananthapuram'),
                ('Kollam', 'Kollam'),
                ('Kochi', 'Kochi'),
                ('Thrissur', 'Thrissur'),
                ('Palakkad', 'Palakkad'),
                ('Malappuram', 'Malappuram'),
                ('Kozhikode', 'Kozhikode'),
                ('Wayanad', 'Wayanad'),
                ('Kannur', 'Kannur'),
                ('Kasaragod', 'Kasaragod'),
                ('Idukki', 'Idukki'),
                ('Ernakulam', 'Ernakulam'),
                ('Alappuzha', 'Alappuzha'),
                ('Pathanamthitta', 'Pathanamthitta'),
            ], attrs={'class': 'form-control'}),
            'market_name': forms.TextInput(attrs={'class': 'form-control'}),
            'price_per_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'trend': forms.Select(attrs={'class': 'form-control'}),
            'market_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class PestDetectionForm(forms.ModelForm):
    class Meta:
        model = PestDetection
        fields = ['image', 'detected_pest', 'confidence', 'treatment_recommendation', 
                  'severity', 'affected_area']
        widgets = {
            'detected_pest': forms.TextInput(attrs={'class': 'form-control'}),
            'confidence': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'treatment_recommendation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'affected_area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class CropRecommendationForm(forms.ModelForm):
    class Meta:
        model = CropRecommendation
        fields = ['soil_ph', 'moisture_level', 'season', 'recommended_crops', 
                  'success_probability', 'expected_yield', 'fertilizer_suggestion', 'irrigation_needs']
        widgets = {
            'soil_ph': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'moisture_level': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'season': forms.Select(attrs={'class': 'form-control'}),
            'recommended_crops': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'success_probability': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'expected_yield': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fertilizer_suggestion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'irrigation_needs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
