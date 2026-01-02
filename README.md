# HikeWeather Advisor 🌤️🥾

Веб-сервис для интеллектуального планирования пеших походов с учетом погодных условий.

**Стек технологий:**
- Python 3.11, Django 4.2.7
- SQLite (разработка), PostgreSQL (продакшен)
- Plotly 5.18.0 для визуализации
- OpenWeatherMap API
- Bootstrap 5

**Как запустить:**
1. `git clone [репозиторий]`
2. `python -m venv venv`
3. `.\venv\Scripts\activate` (Windows)
4. `pip install -r requirements.txt`
5. `python manage.py migrate`
6. `python manage.py runserver`