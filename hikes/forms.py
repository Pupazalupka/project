from django import forms
from django.contrib.auth.models import User
from .models import HikeRoute, PointOfInterest, Review


class HikeRouteForm(forms.ModelForm):
    """Форма для создания и редактирования маршрутов"""
    
    class Meta:
        model = HikeRoute
        fields = [
            'title', 'description', 'length_km', 
            'estimated_time_h', 'difficulty',
            'start_point_lat', 'start_point_lon',
            'finish_point_lat', 'finish_point_lon'
        ]
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Подробно опишите маршрут, что интересного можно увидеть...'
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Например: "Поход к озеру Горное"'
            }),
        }
        labels = {
            'length_km': 'Протяженность (км)',
            'estimated_time_h': 'Примерное время (часы)',
        }


class PointOfInterestForm(forms.ModelForm):
    """Форма для создания точек интереса"""
    
    class Meta:
        model = PointOfInterest
        fields = ['name', 'description', 'coordinates_lat', 'coordinates_lon', 'type', 'routes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'routes': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    """Форма для отзывов"""
    
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Поделитесь впечатлениями о маршруте...'
            }),
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
        }
        labels = {
            'text': 'Ваш отзыв',
        }


class UserRegistrationForm(forms.ModelForm):
    """Форма регистрации пользователя"""
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']