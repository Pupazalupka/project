# Техническое задание на проект: «HikeWeather Advisor»

## 1. Цель проекта
Разработка веб-сервиса для пеших туристов, который решает проблему планирования походов в условиях переменчивой погоды и ограниченной парковочной инфраструктуры. Сервис автоматически оценивает и ранжирует маршруты на основе актуальных погодных данных.

## 2. Роли пользователей
- **Гость:** Просмотр каталога маршрутов, фильтрация, сортировка по актуальному статусу.
- **Авторизованный пользователь:** Персонализированные рекомендации, отзывы, избранное, создание маршрутов.
- **Администратор:** Полный доступ к админ-панели Django.

## 3. Модели данных (сущности)
1. **HikeRoute (Маршрут)**
   - title, description, length_km, estimated_time_h, difficulty
   - start_point_lat, start_point_lon, finish_point_lat, finish_point_lon
   - author (ForeignKey на User), created_at, updated_at

2. **PointOfInterest (Точка интереса)**
   - name, description, coordinates_lat, coordinates_lon, type
   - routes (ManyToManyField к HikeRoute)

3. **Review (Отзыв)**
   - route (ForeignKey на HikeRoute), user (ForeignKey на User)
   - rating (1-5), text, created_at

4. **RouteCheck (Проверка маршрута)**
   - route (ForeignKey на HikeRoute), check_date
   - weather_summary, weather_temp, weather_precipitation
   - parking_status, overall_score (0-100)

## 4. Ключевой функционал (User Stories)
- US1: Просмотр и фильтрация каталога маршрутов с сортировкой по актуальному баллу пригодности
- US2: Детальный просмотр маршрута с графиком прогноза температуры (Plotly) и статусом парковки
- US3: Персонализированные рекомендации маршрутов на основе текущих условий
- US4: Система отзывов и оценок пользователей

## 5. Внешние интеграции и аналитика
1. **Внешнее API:** OpenWeatherMap One Call API 3.0 для получения прогноза погоды
2. **Библиотеки анализа:** Plotly для построения графиков прогноза температуры