from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('register/', views.register, name='register'),
    
    path('hike/create/', views.hike_create, name='hike_create'),
    path('hike/<int:hike_id>/', views.hike_detail, name='hike_detail'),
    path('my-hikes/', views.my_hikes, name='my_hikes'),
    path('favorites/', views.favorites, name='favorites'),
    path('hike/<int:hike_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]