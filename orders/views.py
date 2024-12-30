from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Request, Response, Customer
from .forms import ResponseForm, RequestForm
from django.contrib import messages
from .forms import CustomerRegistrationForm
from django.db.utils import IntegrityError

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
    return render(request, 'orders/create_request.html', {'form': form})

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
    
    return render(request, 'orders/create_response.html', {'form': form, 'request': request_obj})

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

    return render(request, 'orders/request_detail.html', {'request': request_obj, 'form': form, 'responses': responses})

def request_list(request):
    # Извлекаем все заявки
    requests = Request.objects.all()  # Можно использовать фильтрацию или сортировку по дате, если нужно
    return render(request, 'orders/request_list.html', {'requests': requests})

def home(request):
    # Получаем последние 5 заявок, сортируя по дате создания (по убыванию)
    latest_requests = Request.objects.all().order_by('-created_at')[:5]
    return render(request, 'home.html', {'latest_requests': latest_requests})

# def register_customer(request):
#     if request.method == 'POST':
#         form = CustomerRegistrationForm(request.POST)
#         if form.is_valid():
#             customer = form.save(commit=False)
#             customer.address = request.POST.get('address')  # Получаем адрес из скрытого поля
#             customer.save()
#             messages.success(request, "Заказчик успешно зарегистрирован!")
#             return redirect('home')  # Перенаправляем на главную страницу
#         else:
#             messages.error(request, "Ошибка при регистрации.")
#     else:
#         form = CustomerRegistrationForm()
    
#     return render(request, 'orders/register_customer.html', {'form': form})

def register_customer(request):
    if request.method == 'POST':
        email = request.POST['email']
        # Проверка наличия email
        if Customer.objects.filter(email=email).exists():
            return HttpResponse("Этот email уже зарегистрирован.")
        try:
            customer = Customer(email=email, address=request.POST['address'])
            customer.save()
        except IntegrityError:
            return HttpResponse("Ошибка при регистрации. Попробуйте еще раз.")
        return HttpResponse("Пользователь успешно зарегистрирован.")
    return render(request, 'orders/register_customer.html')