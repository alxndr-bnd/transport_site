from django import forms
from .models import Response, CustomUser

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['message']

from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['description', 'desired_date', 'contact_email']  # Укажите нужные поля из модели

# class CustomerRegistrationForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['email']  # Адрес передается через скрытое поле

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email