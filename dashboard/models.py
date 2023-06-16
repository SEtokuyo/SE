from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models import Sum
from django.contrib.auth import get_user_model


# Create your models here.
class User(AbstractUser):
    ROLES = (
        ('customer', '客戶'),
        ('employee', '員工'),
        ('manager', '主管'),
    )

    role = models.CharField(max_length=20, choices=ROLES, default="customer")
    birthday = models.DateField(null=True)
    street = models.CharField(null=True, max_length=100)
    house_number = models.CharField(null=True, max_length=10)
    town = models.CharField(null=True, max_length=100)
    city = models.CharField(null=True, max_length=100)
    news_notification = models.BooleanField(default=False)
    activity_notification = models.BooleanField(default=False)
    promotion_notification = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=100, default='default name')
    description = models.TextField(default='default description')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sales = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default='default category')


    @classmethod
    def get_sales_line_chart_data(cls):
        sales_data = cls.objects.values('created_at__month').annotate(total_sales=Sum('quantity')).order_by('created_at__month')
        months = [data['created_at__month'] for data in sales_data]
        sales = [data['total_sales'] for data in sales_data]

        return {
            'labels': months,
            'data': sales,
        }

    @classmethod
    def get_sales_chart_data(cls):
        total_sales = cls.objects.aggregate(total_sales=Sum('quantity'))['total_sales']
        product_sales = cls.objects.values('name').annotate(sales=Sum('quantity')).order_by('name')

        data = {
            'labels': [sale['name'] for sale in product_sales],
            'data': [sale['sales'] / total_sales * 100 for sale in product_sales],
        }
    
        return data

    @classmethod
    def get_stock_chart_data(cls):
        stock_data = cls.objects.values('category').annotate(total_stock=Sum('stock')).order_by('category')
        chart_labels = [data['category'] for data in stock_data]
        chart_data = [data['total_stock'] for data in stock_data]

        return {
            'labels': chart_labels,
            'data': chart_data,
        }

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(default='')  # 默认为空字符串
    shipping_address = models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    order_items = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_product_sales_percentage(self):
        product_sales = self.order_items_set.values('product__name').annotate(
            sales=Count('product')).order_by('product__name')
        total_sales = sum([sale['sales'] for sale in product_sales])

        data = {
            'labels': [sale['product__name'] for sale in product_sales],
            'data': [sale['sales'] / total_sales * 100 for sale in product_sales],
        }

        return data

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} - {self.product}"   

class Customer(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='customer_photos', default='')  # 默认为空字符串
    first_visit_date = models.DateField()
    remarks = models.TextField()




