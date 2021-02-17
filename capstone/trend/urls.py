from django.urls import path
from . import views

app_name = 'trend'
urlpatterns = [
    path('', views.main, name = 'main')
]