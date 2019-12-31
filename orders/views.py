import json
import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Pizza, Topping, Sub, Pasta, Salad, Platter, Order
from .static.orders.python.generate_order_info import generate_order_info
from .static.orders.python.get_order_items import get_order_items
from .static.orders.python.complete_order import complete_order
from .static.orders.python.mark_completed_orders import mark_completed_orders
from .static.orders.python.populate_new_orders import populate_new_orders
from .static.orders.python.send_completion_emails import send_completion_emails

def staff_check(user):
    return user.is_staff

#### No login views #####
def index_view(request):
    context = { 
        'logged_in': request.user.is_authenticated,
        'staff': request.user.is_staff
    }
    return render(request, 'orders/home.html', context=context)

@login_required(login_url='/login')
def order_view(request):
    context = {
        'menu': [
            {
                'title': 'Pizza',
                'content': Pizza.objects.all()
            },
            {
                'title': 'Subs',
                'content': Sub.objects.all()
            },
            {
                'title': 'Pasta',
                'content': Pasta.objects.all()
            },
            {
                'title': 'Salad',
                'content': Salad.objects.all()
            },
            {
                'title': 'Platter',
                'content': Platter.objects.all()
            },
        ],
        'logged_in': request.user.is_authenticated,
        'staff': request.user.is_staff
    }
    return render(request, 'orders/order.html', context)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'orders/login.html')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('order')
        else:
            return render(request,
                'orders/error.html',
                context={'error': 401,
                'text': 'Username/Password incorrect'})

def register_view(request):
    if request.method == 'GET':
        return render(request, 'orders/register.html')
    if request.method == 'POST':
        form_data = {}
        if 'check' in request.POST:   
            for i in range(8):
                form_data[request.POST['form[{}][name]'.format(i)]] = request.POST['form[{}][value]'.format(i)]
            if form_data['email'] != form_data['confemail']:
                return JsonResponse(data={'error': 'Email and Confirmation must match'})
            if form_data['pass'] != form_data['confpass']:
                return JsonResponse(data={'error': 'Password must match'})
            if User.objects.filter(username=form_data['username']).exists():
                return JsonResponse(data={'error': 'Username is already taken'})
            if User.objects.filter(email=form_data['email']).exists():
                return JsonResponse(data={'error': 'Email is already taken'})
            for field in form_data.values():
                if field == '':
                    return JsonResponse(data={'error': 'Please complete all fields'})
            return JsonResponse({'user_is_unique': True})
        else:
            username = request.POST['username']
            password = request.POST['pass']
            conf_pass = request.POST['confpass']
            email = request.POST['email']
            conf_email = request.POST['confemail']
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            if username == '' or password == '' or email== '' or first_name == '' or last_name == '':
                return render(request, 'orders/error.html', context={'error': 'All fields must be completed'})
            if email != conf_email:
                return render(request, 'orders/error.html', context={'error': 'Email addresses must match'})
            if password != conf_pass:
                return render(request, 'orders/error.html', context={'error': 'Passwords address must match'})
            if User.objects.filter(username=username).exists():
                return render(request, 'orders/error.html', context={'error': 'Username already exists'})
            if User.objects.filter(email=email).exists():
                return render(request, 'orders/error.html', context={'error': 'Email address already exists'})
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            new_user.save()
            login(request, new_user)
            return redirect('order')

def logout_view(request):
    logout(request)
    return redirect('index')

#### Views the require login ####

@login_required(login_url='/login')
def basket_view(request):
    if 'basket' in request.COOKIES.keys():
        order_items = get_order_items(request.COOKIES['basket'])
        order_details = generate_order_info(order_items)
        return render(request, 'orders/basket.html',
            context={
                'order': order_details[0],
                'pizza_toppings': Topping.objects.all(),
                'sub_toppings': Sub.objects.filter(extra=True),
                'total_price': order_details[1],
                'logged_in': request.user.is_authenticated,
                'staff': request.user.is_staff
            })
    else:
        return render(request,
            'orders/basket.html',
            context={
                'empty': True,
                'total_price': '0.00',
                'logged_in': request.user.is_authenticated,
                'staff': request.user.is_staff
            })

@login_required(login_url='/login')
def take_order_view(request):
    order_items = get_order_items(request.COOKIES['ordered'])[0]
    order_number = complete_order(order_items, request.user.username)
    order = Order.objects.filter(order_number=order_number)
    return render(request,
        'orders/success.html',
        context={
            'order': order,
            'logged_in': request.user.is_authenticated,
            'staff': request.user.is_staff
        })

@login_required(login_url='/login')
def my_orders_view(request):
    if request.method == 'GET':
        today = datetime.date.today()
        user_orders = Order.objects.filter(username=request.user.username).filter(date=today)
        return render(request,
        'orders/my_current_orders.html',
        context={
            'user_orders': user_orders,
            'logged_in': request.user.is_authenticated,
            'staff': request.user.is_staff
        })

@login_required(login_url='/login')
def my_orders_history_view(request):
    if request.method == 'GET':
        user_orders = Order.objects.filter(username=request.user.username).order_by('date').reverse()
        return render(request,
        'orders/my_orders_history.html',
        context={
            'user_orders': user_orders,
            'logged_in': request.user.is_authenticated,
            'staff': request.user.is_staff
        })

@login_required(login_url='/login')
def refresh_my_orders_view(request):
    if request.method == "GET":
        current_max_order_id = current_max_order = request.GET['max']
        today = datetime.date.today()
        new_order_queryset = Order.objects.filter(id__gt=current_max_order_id, username=request.user.username).filter(date=today)
        new_orders = populate_new_orders(new_order_queryset)
        completed_orders_queryset = Order.objects.filter(
            id__lte=current_max_order_id,
            username=request.user.username,
            completed=True).filter(date=today)
        completed_orders = populate_new_orders(completed_orders_queryset)
        return JsonResponse({'new_orders': new_orders,'changed_orders': completed_orders})

#### Staff only views ####

@login_required(login_url='/login')
@user_passes_test(staff_check)
def order_list_view(request):
    if request.method == 'GET':
        today = datetime.date.today()
        orders = Order.objects.filter(date=today).order_by('date').reverse()
        return render(request,
            'orders/order_list.html',
            context={
                'orders': orders,
                'logged_in': request.user.is_authenticated,
                'staff': request.user.is_staff
            })

@login_required(login_url='/login')
@user_passes_test(staff_check)
def refresh_order_list_view(request):
    if request.method == "GET":
        current_max_order_id = request.GET['max']
        today = datetime.date.today()
        new_order_queryset = Order.objects.filter(id__gt=current_max_order_id, date=today)
        new_orders = populate_new_orders(new_order_queryset)
        if new_orders != None:
            return JsonResponse({'new_orders': new_orders})
        else:
            return JsonResponse({'error': "No new orders", 'new_orders': []})

@login_required(login_url='/login')
@user_passes_test(staff_check)
def update_order_list_view(request):
    if request.method == 'POST':
        completed_orders = request.POST['completed_orders']
        mark_completed_orders(completed_orders)
        send_completion_emails(completed_orders)
        return JsonResponse({'success': True})

