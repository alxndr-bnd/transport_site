# orders/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # path('', views.request_list, name='request_list'),  # Главная страница для списка заявок
    path('', views.home, name='home'),  # Главная страница
    path('create/', views.create_request, name='create_request'),  # Страница для создания заявки
    path('register/', views.register_customer, name='register_customer'),
    # Другие маршруты
    path('login/', LoginView.as_view(template_name='orders/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]