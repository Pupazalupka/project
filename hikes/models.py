from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class HikeRoute(models.Model):
    """Модель маршрута для пешего похода"""
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Легкий'),
        ('medium', 'Средний'),
        ('hard', 'Сложный'),
    ]
    
    title = models.CharField(
        max_length=200, 
        verbose_name='Название маршрута'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    length_km = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        verbose_name='Протяженность (км)',
        validators=[MinValueValidator(0.1)]
    )
    estimated_time_h = models.PositiveIntegerField(
        verbose_name='Примерное время (часы)',
        validators=[MinValueValidator(1), MaxValueValidator(48)]
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        verbose_name='Сложность'
    )
    
    # Координаты стартовой точки
    start_point_lat = models.FloatField(
        verbose_name='Широта старта'
    )
    start_point_lon = models.FloatField(
        verbose_name='Долгота старта'
    )
    
    # Координаты конечной точки
    finish_point_lat = models.FloatField(
        verbose_name='Широта финиша'
    )
    finish_point_lon = models.FloatField(
        verbose_name='Долгота финиша'
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='hike_routes'
    )
    favorited_by = models.ManyToManyField(
        User,
        related_name='favorite_hikes',
        verbose_name='В избранном у',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_average_rating(self):
        """Возвращает средний рейтинг маршрута"""
        reviews = self.reviews.all()
        if reviews:
            return sum([r.rating for r in reviews]) / len(reviews)
        return 0


class PointOfInterest(models.Model):
    """Модель точки интереса на маршруте"""
    
    TYPE_CHOICES = [
        ('viewpoint', 'Смотровая площадка'),
        ('waterfall', 'Водопад'),
        ('spring', 'Источник'),
        ('camping', 'Кемпинг'),
        ('monument', 'Памятник'),
        ('other', 'Другое'),
    ]
    
    name = models.CharField(
        max_length=100,
        verbose_name='Название точки'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    coordinates_lat = models.FloatField(
        verbose_name='Широта'
    )
    coordinates_lon = models.FloatField(
        verbose_name='Долгота'
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='other',
        verbose_name='Тип точки'
    )
    
    # Связь ManyToMany с маршрутами
    routes = models.ManyToManyField(
        HikeRoute,
        related_name='points_of_interest',
        verbose_name='Маршруты',
        blank=True
    )
    
    class Meta:
        verbose_name = 'Точка интереса'
        verbose_name_plural = 'Точки интереса'
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Review(models.Model):
    """Модель отзыва о маршруте"""
    
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    route = models.ForeignKey(
        HikeRoute,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Маршрут'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва'
    )
    
    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created_at']
        # Один пользователь - один отзыв на маршрут
        unique_together = ['route', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.route.title} ({self.rating}★)"


class RouteCheck(models.Model):
    """Модель для хранения проверок маршрута (кэш данных API)"""
    
    PARKING_STATUS_CHOICES = [
        ('available', 'Свободно'),
        ('limited', 'Ограничено'),
        ('full', 'Занято'),
        ('unknown', 'Нет данных'),
    ]
    
    route = models.ForeignKey(
        HikeRoute,
        on_delete=models.CASCADE,
        related_name='route_checks',
        verbose_name='Маршрут'
    )
    check_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата проверки'
    )
    
    # Данные о погоде
    weather_summary = models.CharField(
        max_length=100,
        verbose_name='Погода'
    )
    weather_temp = models.FloatField(
        verbose_name='Температура (°C)'
    )
    weather_precipitation = models.FloatField(
        verbose_name='Вероятность осадков (%)',
        default=0
    )
    
    # Данные о парковке
    parking_status = models.CharField(
        max_length=20,
        choices=PARKING_STATUS_CHOICES,
        default='unknown',
        verbose_name='Статус парковки'
    )
    
    # Общий балл (0-100)
    overall_score = models.IntegerField(
        verbose_name='Общий балл',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0
    )
    
    class Meta:
        verbose_name = 'Проверка маршрута'
        verbose_name_plural = 'Проверки маршрутов'
        ordering = ['-check_date']
    
    def __str__(self):
        return f"Проверка {self.route.title} - {self.check_date.strftime('%d.%m.%Y %H:%M')}"
