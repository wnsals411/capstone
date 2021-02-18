from django.urls import path
from . import views

app_name = 'qna'
urlpatterns = [
    path('', views.main, name = 'main'),
    path('write/', views.write, name = 'write'),
    path('current_page=<int:page>/', views.pageview, name = 'pageview'),
    path('<int:board_id>/', views.detail, name = 'detail'),
    path('<int:board_id>/delete', views.delete, name = 'delete'),
    path('search/', views.search, name='search'),
]
