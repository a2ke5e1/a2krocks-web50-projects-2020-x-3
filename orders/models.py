from django.db import models
from django.contrib.auth.models import User
from django.core import serializers

SIZE = (
    ('S', 'small'),
    ('L', 'large')
)

ORDER_STATUS = (
    ('p', "PENDING")
    , ('c', "COMPLETED")
)


# Create your models here.

class toppings(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"


class sub(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=32, choices=SIZE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.get_size_display()} - ${self.price}"


class dinner_platter(models.Model):
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=32, choices=SIZE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.get_size_display()} - ${self.price}"


class pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class salad(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price}"


class pizza_types(models.Model):
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=32, choices=SIZE)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    topping_price = models.DecimalField(max_digits=10, decimal_places=2)
    topping_price2 = models.DecimalField(max_digits=10, decimal_places=2)
    topping_price3 = models.DecimalField(max_digits=10, decimal_places=2)
    special_price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.type} - {self.topping_price} - {self.topping_price2} - {self.topping_price3}"


class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salad_name = models.TextField(default="")
    pizza_name = models.TextField(default="")
    dp = models.TextField(default="")
    sub_name = models.TextField(default="")
    pasta_name = models.TextField(default="")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default="0")

    def __str__(self):
        return f"{self.salad_name} - {self.pasta_name} - {self.pizza_name} - {self.dp}- {self.sub_name} -{self.pasta_name} - {self.total_cost}"

class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salad_name = models.TextField(default="")
    pizza_name = models.TextField(default="")
    dp = models.TextField(default="")
    sub_name = models.TextField(default="")
    pasta_name = models.TextField(default="")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    status = models.CharField(choices=ORDER_STATUS, max_length=32)

    def __str__(self):
        return  f"{self.user} - {self.status}"

