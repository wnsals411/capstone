from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.sucess, name='index'),
    path('search/', views.SearchFormView.as_view(), name='search'),
]
