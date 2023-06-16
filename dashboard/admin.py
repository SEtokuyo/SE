from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Product, Order, OrderItem, Customer, Role, Status,PaymentMethod
# Register your models here.


admin.site.register(User)
admin.site.register(Status)
admin.site.register(PaymentMethod)
admin.site.register(Role)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)