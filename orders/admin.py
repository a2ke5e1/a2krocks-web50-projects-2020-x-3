from django.contrib import admin
from .models import sub, pasta, salad, dinner_platter, pizza_types, cart, toppings, order

admin.site.register(pasta)
admin.site.register(sub)
admin.site.register(salad)
admin.site.register(dinner_platter)
admin.site.register(pizza_types)
admin.site.register(toppings)
admin.site.register(order)