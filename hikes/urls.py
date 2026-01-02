from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('recommendations/', views.recommendations, name='recommendations'),
    path('register/', views.register, name='register'),
    
    path('hike/create/', views.hike_create, name='hike_create'),
    path('hike/<int:hike_id>/', views.hike_detail, name='hike_detail'),
    path('hike/<int:hike_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
]