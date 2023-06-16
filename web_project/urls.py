"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic.base import TemplateView
from dashboard.views import dashboard , dashboard_view, signup_view,  settings_view, update_profile, update_notification, order_list, order_detail, order_edit, order_delete, sales_chart_data, stock_chart_data, sales_line_chart_data
from dashboard import views
from datetime import datetime

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', dashboard_view, name='home'),
    path('signup/', signup_view ,name="signup"),
    path('dashboard/', dashboard, name="dashboard"),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:id>/', order_detail, name='order_detail'),
    path('orders/<int:id>/edit/', order_edit, name='order_edit'),
    path('orders/<int:id>/delete/', order_delete, name='order_delete'),
    path('settings/', settings_view, name="settings"),
    path('update_profile/', update_profile, name="update_profile"),
    path('update_notification/', update_notification, name="update_notification"),
    path('sales-chart-data/', sales_chart_data, name='sales_chart_data'),
    path('stock-chart-data/', stock_chart_data, name='stock_chart_data'),
    path('sales-line-chart-data/', sales_line_chart_data, name='sales_line_chart_data'),
    path('customer/', views.customer_view, name='customer'),
]
