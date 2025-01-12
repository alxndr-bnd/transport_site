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

def request_detail(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)
    responses = request_obj.responses.all()

    if request.method == "POST" and user.is_authenticated:
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.request = request_obj
            response.carrier = request.user  # Привязка отклика к пользователю
            response.save()
            messages.success(request, "Отклик отправлен успешно!")
            return redirect('request_detail', request_id=request_obj.id)
    else:
        form = ResponseForm()

    return render(request, 'request_detail.html', {'request': request_obj, 'form': form, 'responses': responses})

