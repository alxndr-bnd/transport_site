# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.request_list, name='request_list'),  # Главная страница для списка заявок
    path('', views.home, name='home'),  # Главная страница
    path('create/', views.create_request, name='create_request'),  # Страница для создания заявки
    path('register/', views.register_customer, name='register_customer'),
]