from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Request, Response, CustomUser
from .forms import ResponseForm, RequestForm, CustomerRegistrationForm, CarrierRegistrationForm

# Create your views here.

def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            # Указываем текущего пользователя в поле created_by
            new_request = form.save(commit=False)
            new_request.created_by = request.user
            new_request.save()
            return redirect('request_list')
    else:
        form = RequestForm()
    return render(request, 'create_request.html', {'form': form})

def create_response(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)  # Находим заявку по ID
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.request = request_obj  # Привязываем отклик к заявке
            response.carrier = request.user  # Привязываем отклик к текущему перевозчику
            response.save()
            return redirect('request_detail', request_id=request_obj.id)  # Перенаправляем на страницу заявки
    else:
        form = ResponseForm()
    
    return render(request, 'create_response.html', {'form': form, 'request': request_obj})

def request_detail(request, request_id):
    request_obj = get_object_or_404(Request, id=request_id)  # Получаем заявку по ID
    responses = request_obj.responses.all()  # Все отклики на заявку

    # Форма отклика
    if request.method == "POST":
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.request = request_obj  # Привязываем отклик к заявке
            response.carrier = request.user  # Привязываем отклик к текущему пользователю (перевозчику)
            response.save()
            return redirect('request_detail', request_id=request_obj.id)  # Перенаправляем на страницу заявки
    else:
        form = ResponseForm()

    # Фильтрация откликов по пользователю
    if request.user == request_obj.created_by:
        responses = request_obj.responses.all()  # Получаем все отклики для заявки

    return render(request, 'request_detail.html', {'request': request_obj, 'form': form, 'responses': responses})


def request_list(request):
    # Извлекаем все заявки
    requests = Request.objects.all()  # Можно использовать фильтрацию или сортировку по дате, если нужно
    return render(request, 'request_list.html', {'requests': requests})

def home(request):
    # Получаем последние 5 заявок, сортируя по дате создания (по убыванию)
    latest_requests = Request.objects.all().order_by('-created_at')[:5]
    return render(request, 'home.html', {'latest_requests': latest_requests})

def register_customer(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Сохраняем объект, не сохраняя в базу
            generated_password = user.set_random_password()  # Генерируем пароль
            user.set_password(generated_password)  # Устанавливаем хэшированный пароль
            user.save()  # Сохраняем пользователя с новым паролем
            return render(request, 'success.html', {'form': form})
            # messages.success(request, "Пользователь успешно зарегистрирован.")    
    else:
        form = CustomerRegistrationForm()
    return render(request, 'register_customer.html', {'form': form})

@login_required
def user_orders(request):
    user_orders = Request.objects.filter(created_by=request.user)  # Заказы текущего пользователя
    return render(request, 'user_orders.html', {'orders': user_orders})

def register_carrier(request):
    if request.method == 'POST':
        form = CarrierRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не сохраняем еще пользователя
            generated_password = user.set_random_password()  # Генерируем пароль
            user.set_password(generated_password)  # Устанавливаем хэшированный пароль
            user.role = CustomUser.Roles.CARRIER  # Присвоить роль
            user.save()  # Сохраняем пользователя с новым паролем
            messages.success(request, "Перевозчик успешно зарегистрирован.")
            return render(request, 'success.html', {'form': form})
    else:
        form = CarrierRegistrationForm()

    return render(request, 'register_carrier.html', {'form': form})

def accept_response(request, response_id):
    response = get_object_or_404(Response, id=response_id)
    if request.user == response.request.created_by:
        response.is_accepted = True
        response.save()
    return redirect('request_detail', request_id=response.request.id)