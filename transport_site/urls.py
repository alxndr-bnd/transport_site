"""
URL configuration for transport_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Главная страница
    path('request/<int:request_id>/respond/', views.create_response, name='create_response'),
    path('request/<int:request_id>/', views.request_detail, name='request_detail'),
    path('create/', views.create_request, name='create_request'),
    path('requests/', views.request_list, name='request_list'),  # Список заявок
    path('', include('orders.urls')),  # Подключаем URLs приложения orders
]

