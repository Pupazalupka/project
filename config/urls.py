from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('hikes.urls')),
    # Добавляем стандартные пути для аутентификации
    path('login/', auth_views.LoginView.as_view(template_name='hikes/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]