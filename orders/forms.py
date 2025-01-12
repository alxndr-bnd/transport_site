from django import forms
from .models import Response, CustomUser, Request


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        price = forms.DecimalField(max_digits=5, decimal_places=0, required=True, label="Цена перевозки")
        fields = ['price']

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['description', 'desired_date', 'contact_email']  # Укажите нужные поля из модели

class CustomerRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email
    
class CarrierRegistrationForm(forms.ModelForm):
    license_number = forms.CharField(max_length=100, required=True, label="Номер лицензии")
    vehicle_details = forms.CharField(widget=forms.Textarea, required=True, label="Детали транспортных средств")

    class Meta:
        model = CustomUser
        fields = ['email', 'license_number', 'vehicle_details']
