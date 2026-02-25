from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    SupplierProfile, SupplierProduct, SupplyOrder, OrderItem, 
    SupplierReview, SupplierAvailability, SupplierServiceArea
)


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'})
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
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user


class SupplierRegistrationForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = ['business_name', 'business_type', 'description', 'location', 'address', 
                 'phone_number', 'email', 'website', 'established_year', 'certifications']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business name'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Describe your business and specialties'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City/District'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Full business address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Business email'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website (optional)'}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control', 'min': 1950, 'max': 2024}),
            'certifications': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_established_year(self):
        year = self.cleaned_data.get('established_year')
        if year and (year < 1950 or year > 2024):
            raise forms.ValidationError("Please enter a valid year between 1950 and 2024.")
        return year


class SupplierProductForm(forms.ModelForm):
    class Meta:
        model = SupplierProduct
        fields = ['name', 'category', 'description', 'price', 'unit', 'min_order_quantity', 
                 'max_order_quantity', 'availability_status', 'stock_quantity', 'is_featured', 
                 'is_organic', 'delivery_time_days', 'return_policy']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Detailed product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., kg, liters, pieces'}),
            'min_order_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'max_order_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_organic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'delivery_time_days': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'return_policy': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Return and exchange policy'}),
        }
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price


class SupplierProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = SupplierProfile
        fields = ['business_name', 'business_type', 'description', 'location', 'address', 
                 'phone_number', 'email', 'website', 'certifications', 'is_active']
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control'}),
            'business_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'certifications': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class SupplyOrderForm(forms.Form):
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Delivery address'})
    )
    delivery_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Special delivery instructions (optional)'})
    )
    expected_delivery_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


class SupplierServiceAreaForm(forms.ModelForm):
    class Meta:
        model = SupplierServiceArea
        fields = ['district', 'taluk', 'villages', 'delivery_charge', 'min_order_amount']
        widgets = {
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kerala district'}),
            'taluk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Taluk within district'}),
            'villages': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'List of villages served'}),
            'delivery_charge': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
            'min_order_amount': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': '0.01'}),
        }
