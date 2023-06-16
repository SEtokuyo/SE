import random
import string
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
from dashboard.models import Role, Product, User, Customer, Order, OrderItem


class Command(BaseCommand):
    help = 'Generate fake data for testing.'

    def handle(self, *args, **kwargs):
        fake = Faker()
        User = get_user_model()

        # Create roles
        roles = ['Admin', 'Staff', 'Customer']
        for role_name in roles:
            Role.objects.create(name=role_name)

        # Create users
        for _ in range(10):
            username = fake.user_name()
            password = fake.password()
            role = random.choice(Role.objects.all())
            User.objects.create_user(
                username=username, password=password, role=role)

        # Create products
        for _ in range(20):
            name = fake.word()
            description = fake.sentence()
            price = random.uniform(1, 100)
            quantity = random.randint(1, 100)
            sales = random.uniform(0, 100)
            stock = random.randint(0, 100)
            category = random.choice(
                ['Category A', 'Category B', 'Category C'])
            Product.objects.create(name=name, description=description, price=price, quantity=quantity,
                                   sales=sales, stock=stock, category=category)

        # Create customers
        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            name = f'{first_name} {last_name}'
            contact_number = fake.phone_number()
            address = fake.address()
            email = fake.email()
            user = random.choice(User.objects.filter(role__name='Customer'))
            first_visit_date = fake.date_between('-2 years', 'today')
            remarks = fake.paragraph()
            Customer.objects.create(name=name, contact_number=contact_number, address=address, email=email,
                                    user=user, first_visit_date=first_visit_date, remarks=remarks)

        # Create orders
        for _ in range(10):
            customer = random.choice(Customer.objects.all())
            total_amount = random.uniform(1, 1000)
            shipping_address = fake.address()
            order = Order.objects.create(
                customer=customer, total_amount=total_amount, shipping_address=shipping_address)

            # Create order items
            products = random.sample(
                list(Product.objects.all()), random.randint(1, 5))
            for product in products:
                quantity = random.randint(1, 10)
                price = product.price
                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity, price=price)

        self.stdout.write(self.style.SUCCESS(
            'Fake data generated successfully.'))
