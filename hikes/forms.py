from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import HikeRoute, Review

class HikeRouteForm(forms.ModelForm):
    class Meta:
        model = HikeRoute
        fields = [
            'title', 'description', 'length_km', 
            'estimated_time_h', 'difficulty',
            'start_point_lat', 'start_point_lon',
            'finish_point_lat', 'finish_point_lon'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(),
            'text': forms.Textarea(attrs={'rows': 4}),
        }

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']