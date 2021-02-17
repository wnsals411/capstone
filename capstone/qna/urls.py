from django.urls import path
from . import views

app_name = 'qna'
urlpatterns = [
    path('', views.main, name = 'main')
]