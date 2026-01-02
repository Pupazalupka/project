import random
from datetime import datetime, timedelta
from django.utils import timezone

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