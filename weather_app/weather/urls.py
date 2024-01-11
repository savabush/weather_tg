from django.urls import path

from weather import views

urlpatterns = [
    path('', views.WeatherView.as_view(), name='index'),
]