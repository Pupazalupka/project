from django.contrib import admin
from .models import HikeRoute, PointOfInterest, Review, RouteCheck


@admin.register(HikeRoute)
class HikeRouteAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'length_km', 'author', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'author')
        }),
        ('Параметры маршрута', {
            'fields': ('length_km', 'estimated_time_h', 'difficulty')
        }),
        ('Координаты', {
            'fields': ('start_point_lat', 'start_point_lon', 
                      'finish_point_lat', 'finish_point_lon')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'coordinates_lat', 'coordinates_lon')
    list_filter = ('type',)
    search_fields = ('name', 'description')
    filter_horizontal = ('routes',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('route', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('route__title', 'user__username', 'text')


@admin.register(RouteCheck)
class RouteCheckAdmin(admin.ModelAdmin):
    list_display = ('route', 'check_date', 'weather_summary', 
                   'weather_temp', 'parking_status', 'overall_score')
    list_filter = ('parking_status', 'check_date')
    readonly_fields = ('check_date',)
