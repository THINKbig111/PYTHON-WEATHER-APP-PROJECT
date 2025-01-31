from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('get_weather/', views.get_weather, name='get_weather'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('calculate-distance/', views.distance_calculation, name='calculate_distance'),
    path('contact/', views.contact, name='contact'),
    path('profile_update/', views.profile_update, name='profile_update'),

]
