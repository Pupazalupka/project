from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.core.paginator import Paginator
from .models import HikeRoute, PointOfInterest, Review, RouteCheck
from .forms import HikeRouteForm, PointOfInterestForm, ReviewForm, UserRegistrationForm
import requests
from django.conf import settings


def home(request):
    """Главная страница со списком маршрутов"""
    # Получаем все маршруты с аннотациями
    hikes = HikeRoute.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        reviews_count=Count('reviews')
    ).order_by('-created_at')
    
    # Фильтрация по сложности
    difficulty = request.GET.get('difficulty')
    if difficulty and difficulty in ['easy', 'medium', 'hard']:
        hikes = hikes.filter(difficulty=difficulty)
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        hikes = hikes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Пагинация
    paginator = Paginator(hikes, 9)  # 9 маршрутов на странице
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
    hike = get_object_or_404(
        HikeRoute.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            reviews_count=Count('reviews')
        ),
        id=hike_id
    )
    
    # Получаем точки интереса для этого маршрута
    points = hike.points_of_interest.all()
    
    # Получаем отзывы
    reviews = hike.reviews.all().order_by('-created_at')[:10]
    
    # Проверяем, оставлял ли текущий пользователь отзыв
    user_review = None
    if request.user.is_authenticated:
        user_review = Review.objects.filter(route=hike, user=request.user).first()
    
    # Форма для отзыва (если пользователь еще не оставлял)
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
    
    # Получаем последнюю проверку маршрута (данные API)
    latest_check = hike.route_checks.order_by('-check_date').first()
    
    # Генерируем тестовые данные для графика (позже заменим на реальные из API)
    weather_data = {
        'labels': ['9:00', '12:00', '15:00', '18:00', '21:00'],
        'temperatures': [15, 18, 20, 17, 14],
    }
    
    context = {
        'hike': hike,
        'points': points,
        'reviews': reviews,
        'user_review': user_review,
        'review_form': review_form,
        'latest_check': latest_check,
        'weather_data': weather_data,
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