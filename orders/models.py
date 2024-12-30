from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

# Create your models here.

# Модель пользователя
class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        CUSTOMER = 'customer', _('Заказчик')
        CARRIER = 'carrier', _('Перевозчик')

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.CUSTOMER,
    )

class Customer(models.Model):
    email = models.EmailField()
    address = models.TextField()  # Храним полный адрес

    def __str__(self):
        return self.email

# Модель заявки
class Request(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название заявки")
    description = models.TextField(verbose_name="Описание объекта перевозки")
    desired_date = models.DateField(verbose_name="Желаемая дата перевозки")
    contact_email = models.EmailField(verbose_name="Контактный email")
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="requests",
        verbose_name="Создатель заявки",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Status(models.TextChoices):
        OPEN = 'open', _('Открыта')
        IN_PROGRESS = 'in_progress', _('В процессе')
        CLOSED = 'closed', _('Закрыта')

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        verbose_name="Статус заявки",
    )

class Response(models.Model):
    request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='responses')  # Связь с заявкой
    carrier = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # Перевозчик, откликнувшийся на заявку
    message = models.TextField()  # Сообщение перевозчика
    responded_at = models.DateTimeField(auto_now_add=True)  # Время отклика

    def __str__(self):
        return f"Response by {self.carrier.username} for {self.request.title}"

    def __str__(self):
        return self.title