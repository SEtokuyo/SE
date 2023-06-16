from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order, Product

class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='密碼', widget=forms.PasswordInput)
    password2 = forms.CharField(label='確認密碼', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            password2 = password2.strip()  # 去除空白

        if password1 != password2:
            raise forms.ValidationError('確認密碼不相符')

        return password2
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birthday', 'street', 'house_number', 'town', 'city']


class NotificationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['news_notification',
                  'activity_notification', 'promotion_notification']
        from django import forms


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'total_amount']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price',
                  'quantity', 'stock', 'category']
        labels = {
            'name': '產品名稱',
            'description': '產品描述',
            'price': '價格',
            'quantity': '數量',
            'stock': '庫存',
            'category': '分類',
        }
