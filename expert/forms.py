from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ExpertProfile, ExpertAdvice

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
            
        return password2
    
    def save(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, password=password)
        return user

class ExpertRegistrationForm(forms.ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['specialization', 'qualifications', 'experience_years', 'bio', 
                 'phone_number', 'location', 'consultation_fee']
        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-select'}),
            'qualifications': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your educational qualifications and certifications', 'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'min': 0, 'max': 50, 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us about your expertise', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Your contact number', 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'placeholder': 'City / Region', 'class': 'form-control'}),
            'consultation_fee': forms.NumberInput(attrs={'min': 0, 'step': '0.01', 'value': '0', 'class': 'form-control'}),
        }
    
    def clean_qualifications(self):
        qualifications = self.cleaned_data.get('qualifications')
        if len(qualifications) < 3:
            raise forms.ValidationError("Qualifications must be at least 3 characters long.")
        return qualifications
    
    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) < 5:
            raise forms.ValidationError("Bio must be at least 5 characters long.")
        return bio
    
    def clean_experience_years(self):
        experience_years = self.cleaned_data.get('experience_years')
        if experience_years < 0 or experience_years > 50:
            raise forms.ValidationError("Experience years must be between 0 and 50.")
        return experience_years
    
    def clean_consultation_fee(self):
        consultation_fee = self.cleaned_data.get('consultation_fee')
        if consultation_fee < 0:
            raise forms.ValidationError("Consultation fee cannot be negative.")
        return consultation_fee

class ExpertProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = ExpertProfile
        fields = ['specialization', 'qualifications', 'experience_years', 'bio', 
                 'phone_number', 'location', 'consultation_fee', 'is_available']
        widgets = {
            'specialization': forms.Select(attrs={'class': 'form-select'}),
            'qualifications': forms.Textarea(attrs={'rows': 3}),
            'experience_years': forms.NumberInput(attrs={'min': 0, 'max': 50}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Your contact number'}),
            'location': forms.TextInput(attrs={'placeholder': 'City / Region'}),
            'consultation_fee': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ConsultationMessageForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type your message here...'}))

class ExpertAdviceForm(forms.ModelForm):
    class Meta:
        model = ExpertAdvice
        fields = ['advice_type', 'title', 'content', 'recommendations', 'follow_up_required', 'follow_up_date']
        widgets = {
            'advice_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'placeholder': 'Advice title'}),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Detailed advice content'}),
            'recommendations': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Specific recommendations for the farmer'}),
            'follow_up_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
        }
