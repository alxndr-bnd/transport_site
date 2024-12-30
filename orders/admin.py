from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Request, Response

# Регистрируем кастомного пользователя
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

# Регистрируем модель CustomUser с использованием кастомного админа
admin.site.register(CustomUser, CustomUserAdmin)

# Регистрируем модель заявки Request
admin.site.register(Request)

class RequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'requested_date', 'customer', 'status']
    list_filter = ['status', 'requested_date', 'customer']  # Фильтры по статусу, дате и заказчику
    search_fields = ['title', 'description']
    ordering = ['requested_date']

class ResponseAdmin(admin.ModelAdmin):
    list_display = ['carrier', 'request', 'responded_at']
    list_filter = ['carrier', 'responded_at']
    search_fields = ['carrier__username', 'request__title']
    ordering = ['responded_at']

admin.site.register(Response, ResponseAdmin)
