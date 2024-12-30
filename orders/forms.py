from django import forms
from .models import Response, Customer

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message']

from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['description', 'desired_date', 'contact_email']  # Укажите нужные поля из модели

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email']  # Адрес передается через скрытое поле