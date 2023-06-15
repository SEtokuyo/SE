from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


# Create your models here.
class User(AbstractUser):
    birthday = models.DateField(null=True)
    street = models.CharField(null=True, max_length=100)
    house_number = models.CharField(null=True, max_length=10)
    town = models.CharField(null=True, max_length=100)
    city = models.CharField(null=True, max_length=100)
    news_notification = models.BooleanField(null=True, default=False)
    activity_notification = models.BooleanField(null=True, default=False)
    promotion_notification = models.BooleanField(null=True, default=False)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    # ...

    @classmethod
    def get_sales_chart_data(cls):
        # 獲取產品收入數據並處理成適合圖表的格式
        sales_data = cls.objects.values('month').annotate(total_sales=Sum('sales')).order_by('month')
        chart_labels = [data['month'] for data in sales_data]
        chart_data = [data['total_sales'] for data in sales_data]

        return {
            'labels': chart_labels,
            'data': chart_data,
        }

    @classmethod
    def get_stock_chart_data(cls):
        # 獲取產品庫存數據並處理成適合圖表的格式
        stock_data = cls.objects.values('category').annotate(total_stock=Sum('stock')).order_by('category')
        chart_labels = [data['category'] for data in stock_data]
        chart_data = [data['total_stock'] for data in stock_data]

        return {
            'labels': chart_labels,
            'data': chart_data,
        }

    # 添加其他圖表所需的模型方法或管理器方法

    @classmethod
    def get_sales_line_chart_data(cls):
        # 獲取銷售折線圖數據並處理成適合圖表的格式
        sales_data = cls.objects.values('month').annotate(total_sales=Sum('sales')).order_by('month')
        chart_labels = [data['month'] for data in sales_data]
        chart_data = [data['total_sales'] for data in sales_data]

        return {
            'labels': chart_labels,
            'data': chart_data,
        }
