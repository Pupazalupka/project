import os
import django
from django.contrib.auth.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Создаем тестового пользователя
if not User.objects.filter(username='testuser').exists():
    User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    print("Создан тестовый пользователь: testuser / testpass123")

# Создаем суперпользователя для админки
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123'
    )
    print("Создан суперпользователь: admin / admin123")

print("Настройка завершена!")