from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Order,Customer
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import ProfileForm, NotificationForm, RegistrationForm, OrderForm
from datetime import datetime
# Create your views here.

def dashboard(request):
    return render(request, 'dashboard.html')

def stock_chart_data(request):
    # 實現產品庫存圖表數據的邏輯
    # 從 Product 模型中獲取庫存數據
    stock_data = Product.get_stock_chart_data()

    # 組織庫存數據為 labels 和 data
    labels = stock_data['labels']
    data = stock_data['data']

    # 構建回傳的 data 字典
    data = {
        "labels": ["Category 1", "Category 2", "Category 3"],
        "labels": labels,
        "data": data
    }

    return JsonResponse(data)

def sales_line_chart_data(request):
    # Retrieve the sales data from the database
    from django.db import models
    products = Product.objects.all()
    sales_data = []
    labels = []

    # Calculate the sales data for each month
    for i in range(1, 13):
        month_sales = products.filter(created_at__month=i).aggregate(
            total_sales=models.Sum(models.F('price') * models.F('quantity')))['total_sales']
        sales_data.append(month_sales if month_sales else 0)
        labels.append(datetime(2000, i, 1).strftime('%b'))
    
    # Return the sales data and labels
    return JsonResponse({'labels': labels, 'data': sales_data})

def sales_chart_data(request):
    from django.db import models
    # 實現銷售圖表數據的邏輯
    # 從 Product 模型中獲取銷售數據
    sales_data = Product.get_sales_chart_data()

    # 組織銷售數據為 labels 和 data
    labels = sales_data['labels']
    data = [sale * 100 for sale in sales_data['data']]  # 將銷售數據轉換為百分比

    # 構建回傳的 data 字典
    data = {
        "labels": labels,
        "data": data
    }
    return JsonResponse(data)

def signup_view(request):
    User = get_user_model()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 檢查使用者名稱是否已存在
            username = form.cleaned_data.get('username')
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, '該使用者名稱已被使用。請選擇其他使用者名稱。')
            else:
                form.save()
                messages.success(request, '註冊成功！')
                print(form.errors)
                return redirect('home')
        else:
            messages.error(request, '註冊失敗。請檢查輸入內容。')
            print(form.errors)
    else:
        form = RegistrationForm()
        print(form.errors)
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})

def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    return render(request, 'order_detail.html', {'order': order})


def order_edit(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_detail', id=order.id)
    else:
        form = OrderForm(instance=order)
    return render(request, 'order_edit.html', {'form': form, 'order': order})

def order_delete(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'order_delete.html', {'order': order})

@login_required
def dashboard_view(request):
    # 在這裡處理從後端獲取數據等相關邏輯
    context = {
        # 將需要傳遞到模板中的變數添加到context字典中
        'total_sales': 10000,
        'best_selling_product': 'Product A',
        # 其他變數...
    }
    return render(request, 'dashboard.html', context)

@login_required
def settings_view(request):
    user = request.user

    profile_form = ProfileForm(instance=user)
    notification_form = NotificationForm(instance=user)

    context = {
        'profile_form': profile_form,
        'notification_form': notification_form,
    }

    return render(request, 'settings.html', context)

@login_required
def update_profile(request):
    user = request.user

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "成功更新個人資料。")
        else:
            messages.error(request, "無法更新個人資料。")
    else:
        profile_form = ProfileForm(instance=user)

    context = {
        'profile_form': profile_form,
    }

    return render(request, 'settings.html', context)

@login_required
def update_notification(request):
    user = request.user

    if request.method == 'POST':
        notification_form = NotificationForm(request.POST, instance=user)
        if notification_form.is_valid():
            notification_form.save()
            messages.success(request, "成功更新通知設定。")
        else:
            messages.error(request, "無法更新通知設定。")
    else:
        notification_form = NotificationForm(instance=user)

    context = {
        'notification_form': notification_form,
    }
 
def customer_view(request):
    customers = Customer.objects.all()
    return render(request, 'customer.html', {'customers': customers})