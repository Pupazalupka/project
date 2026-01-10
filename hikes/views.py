from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator

import random
from datetime import datetime, timedelta
from django.utils import timezone

from .models import HikeRoute, PointOfInterest, Review
from .forms import HikeRouteForm, ReviewForm, UserRegistrationForm


class WeatherService:
    """Сервис для работы с погодными данными"""
    
    @staticmethod
    def get_demo_weather_data(lat, lon):
        """
        Генерирует демо-данные о погоде для заданных координат
        В реальном проекте здесь будет запрос к OpenWeatherMap API
        """
        # Генерируем реалистичные данные
        base_temp = random.randint(10, 25)  # Базовая температура
        
        # Время для графика (ближайшие 12 часов)
        times = []
        temps = []
        current_time = datetime.now()
        
        for i in range(12):
            hour = (current_time + timedelta(hours=i)).strftime('%H:00')
            times.append(hour)
            
            # Температура меняется по синусоиде в течение дня
            hour_of_day = (current_time.hour + i) % 24
            temp_variation = 5 * (1 - abs(hour_of_day - 12) / 12)  # Пик в 12 часов
            temp = base_temp + temp_variation + random.uniform(-2, 2)
            temps.append(round(temp, 1))
        
        # Описание погоды в зависимости от температуры
        if base_temp < 15:
            description = "Прохладно, возьмите куртку"
            icon = "cloud"
        elif base_temp < 20:
            description = "Комфортно, идеально для похода"
            icon = "sun-cloud"
        else:
            description = "Тепло, возьмите воду"
            icon = "sun"
        
        # Вероятность осадков
        precipitation = random.randint(0, 50)
        
        return {
            'current': {
                'temperature': base_temp,
                'feels_like': base_temp - random.randint(0, 3),
                'description': description,
                'icon': icon,
                'humidity': random.randint(40, 80),
                'wind_speed': random.randint(1, 10),
                'precipitation_chance': precipitation,
            },
            'forecast': {
                'labels': times,
                'temperatures': temps,
                'precipitation': [random.randint(0, precipitation) for _ in range(12)],
            }
        }
    
    @staticmethod
    def get_weather_quality_score(weather_data):
        """Рассчитывает балл качества погоды от 0 до 100"""
        current = weather_data['current']
        
        score = 100
        
        # Штраф за осадки
        score -= current['precipitation_chance']
        
        # Штраф за сильный ветер
        if current['wind_speed'] > 8:
            score -= 20
        elif current['wind_speed'] > 5:
            score -= 10
        
        # Бонус за комфортную температуру (15-25°C)
        if 15 <= current['temperature'] <= 25:
            score += 10
        elif current['temperature'] < 5 or current['temperature'] > 30:
            score -= 20
        
        return max(0, min(100, score))


class ParkingService:
    """Сервис для работы с данными о парковках"""
    
    @staticmethod
    def get_parking_status(lat, lon):
        """
        Генерирует демо-статус парковки
        В реальном проекте здесь будет запрос к Google Maps API
        """
        current_hour = datetime.now().hour
        
        # Логика: утром парковки заняты, днем свободны
        if 7 <= current_hour <= 9:
            status = 'busy'
            description = 'Утренний час пик, мало мест'
            score = 40
        elif 9 < current_hour <= 17:
            status = 'available'
            description = 'Достаточно свободных мест'
            score = 80
        elif 17 < current_hour <= 20:
            status = 'limited'
            description = 'Вечерний наплыв, места есть'
            score = 60
        else:
            status = 'available'
            description = 'Ночью много свободных мест'
            score = 90
        
        # Добавляем случайность для реалистичности
        if random.random() < 0.2:
            status = random.choice(['available', 'limited', 'busy'])
            score = random.randint(30, 95)
        
        status_texts = {
            'available': 'Свободно',
            'limited': 'Ограничено',
            'busy': 'Занято',
        }
        
        return {
            'status': status,
            'status_text': status_texts.get(status, 'Неизвестно'),
            'description': description,
            'score': score,
            'last_checked': timezone.now().strftime('%H:%M'),
        }


class RouteAnalyzer:
    """Анализатор маршрутов"""
    
    @staticmethod
    def calculate_overall_score(route, weather_score, parking_score):
        """Рассчитывает общий балл маршрута (0-100)"""
        # Веса: погода 50%, парковка 30%, сложность 20%
        weather_weight = 0.5
        parking_weight = 0.3
        difficulty_weight = 0.2
        
        # Балл за сложность (легкие маршруты получают больше баллов)
        difficulty_scores = {
            'easy': 90,
            'medium': 70,
            'hard': 50,
        }
        difficulty_score = difficulty_scores.get(route.difficulty, 50)
        
        # Расчет общего балла
        total_score = (
            weather_score * weather_weight +
            parking_score * parking_weight +
            difficulty_score * difficulty_weight
        )
        
        return {
            'overall_score': round(total_score),
            'weather_score': weather_score,
            'parking_score': parking_score,
            'difficulty_score': difficulty_score,
            'breakdown': {
                'weather': f"{weather_score}/100 ({weather_weight*100}%)",
                'parking': f"{parking_score}/100 ({parking_weight*100}%)",
                'difficulty': f"{difficulty_score}/100 ({difficulty_weight*100}%)",
            }
        }


def home(request):
    """Главная страница со списком маршрутов"""
    # Получаем все маршруты с аннотациями
    hikes_list = HikeRoute.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    ).order_by('-created_at')
    
    # Фильтрация по сложности
    difficulty = request.GET.get('difficulty')
    if difficulty and difficulty in ['easy', 'medium', 'hard']:
        hikes_list = hikes_list.filter(difficulty=difficulty)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        hikes_list = hikes_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(hikes_list, 9)  # 9 маршрутов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'difficulty_filter': difficulty,
        'search_query': search_query,
    }
    return render(request, 'hikes/home.html', context)


def hike_detail(request, hike_id):
    """Детальная страница маршрута"""
    # Получаем маршрут с аннотациями
    hike = get_object_or_404(
        HikeRoute.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            reviews_count=Count('reviews'),
            favorites_count=Count('favorited_by')
        ),
        id=hike_id
    )
    
    # Получаем точки интереса
    points = hike.points_of_interest.all()
    
    # Получаем отзывы
    reviews = hike.reviews.all().select_related('user').order_by('-created_at')[:10]
    
    # Проверяем, оставлял ли текущий пользователь отзыв
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(route=hike, user=request.user).first()
    
    # Форма для отзыва
    review_form = None
    if request.user.is_authenticated and not user_review:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.route = hike
                review.user = request.user
                review.save()
                messages.success(request, 'Ваш отзыв добавлен!')
                return redirect('hike_detail', hike_id=hike.id)
        else:
            review_form = ReviewForm()
    
    # ====== API ИНТЕГРАЦИЯ ======
    # 1. Получаем данные о погоде
    weather_data = WeatherService.get_demo_weather_data(
        hike.start_point_lat,
        hike.start_point_lon
    )
    
    # 2. Получаем статус парковки
    parking_data = ParkingService.get_parking_status(
        hike.start_point_lat,
        hike.start_point_lon
    )
    
    # 3. Рассчитываем баллы
    weather_score = WeatherService.get_weather_quality_score(weather_data)
    analysis = RouteAnalyzer.calculate_overall_score(
        hike,
        weather_score,
        parking_data['score']
    )
    
    # 4. Подготавливаем данные для графика Plotly
    chart_data = {
        'labels': weather_data['forecast']['labels'],
        'temperatures': weather_data['forecast']['temperatures'],
        'precipitation': weather_data['forecast']['precipitation'],
    }
    
    # Подготавливаем контекст
    context = {
        'hike': hike,
        'points': points,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
        
        # API данные
        'weather': weather_data['current'],
        'parking': parking_data,
        'analysis': analysis,
        'chart_data': chart_data,
        
        # Флаги для интерфейса
        'is_favorited': request.user in hike.favorited_by.all() if request.user.is_authenticated else False,
    }
    
    return render(request, 'hikes/hike_detail.html', context)


@login_required
def hike_create(request):
    """Создание нового маршрута"""
    if request.method == 'POST':
        form = HikeRouteForm(request.POST)
        if form.is_valid():
            hike = form.save(commit=False)
            hike.author = request.user
            hike.save()
            messages.success(request, 'Маршрут успешно создан!')
            return redirect('hike_detail', hike_id=hike.id)
    else:
        form = HikeRouteForm()
    
    return render(request, 'hikes/hike_form.html', {'form': form})


@login_required
def add_to_favorites(request, hike_id):
    """Добавление маршрута в избранное"""
    hike = get_object_or_404(HikeRoute, id=hike_id)
    
    if request.user in hike.favorited_by.all():
        hike.favorited_by.remove(request.user)
        messages.info(request, 'Маршрут удален из избранного')
    else:
        hike.favorited_by.add(request.user)
        messages.success(request, 'Маршрут добавлен в избранное!')
    
    return redirect('hike_detail', hike_id=hike.id)


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Автоматический вход после регистрации
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'hikes/register.html', {'form': form})


def recommendations(request):
    """Страница рекомендаций маршрутов"""
    # Пока возвращаем просто топ маршрутов по рейтингу
    # Позже добавим логику с погодой и парковками
    
    recommended_hikes = HikeRoute.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    ).filter(reviews_count__gte=1).order_by('-avg_rating')[:5]
    
    context = {
        'recommended_hikes': recommended_hikes,
    }
    return render(request, 'hikes/recommendations.html', context)


def about(request):
    """Страница "О проекте" """
    stats = {
        'total_hikes': HikeRoute.objects.count(),
        'total_points': PointOfInterest.objects.count(),
        'total_reviews': Review.objects.count(),
    }
    
    return render(request, 'hikes/about.html', {'stats': stats})