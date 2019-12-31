from django.contrib import admin

from .models import Order,Pizza, Topping, Pasta, Sub, Salad, Platter

admin.site.register(Order)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Pasta)
admin.site.register(Sub)
admin.site.register(Salad)
admin.site.register(Platter)