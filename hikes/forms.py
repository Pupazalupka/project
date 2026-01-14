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
    """Форма для отзыва с оценкой"""
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(attrs={'class': 'star-rating'}),
            'text': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Поделитесь впечатлениями о маршруте...',
                'class': 'form-control'
            }),
        }
        labels = {
            'rating': 'Ваша оценка',
            'text': 'Комментарий (необязательно)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Кастомизируем отображение оценок
        self.fields['rating'].widget.choices = [
            (1, '★☆☆☆☆ - Ужасно'),
            (2, '★★☆☆☆ - Плохо'),
            (3, '★★★☆☆ - Нормально'),
            (4, '★★★★☆ - Хорошо'),
            (5, '★★★★★ - Отлично'),
        ]


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