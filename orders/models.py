from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Topping(models.Model):
    name = models.CharField('Topping', max_length=16)

    def __str__(self):
        return '{}'.format(self.name)

class Pizza(models.Model):
        base = models.CharField('Base', max_length=32, default="Regular")
        item_name = models.CharField('Item', max_length=128)
        small_price = models.DecimalField('Small Price', decimal_places=2, max_digits=4)
        large_price = models.DecimalField('Large Price', decimal_places=2, max_digits=4)
        number_of_toppings = models.IntegerField('Extra Toppings', default=0)
        def __str__(self):
            return '{} small: ${} large: ${}'.format(self.item_name, self.small_price, self.large_price)

class Sub(models.Model):
        item_name = models.CharField('Item', max_length=128)
        small_price = models.DecimalField('Small Price', decimal_places=2, max_digits=4, null=0)
        large_price = models.DecimalField('Large Price', decimal_places=2, max_digits=4)
        extra = models.BooleanField('Is Extra', null=False, default=None)
        def __str__(self):
            return '{} small: ${} large: ${}'.format(self.item_name, self.small_price, self.large_price)

class Pasta(models.Model):
        item_name = models.CharField('Item', max_length=128)
        small_price = models.DecimalField('Small Price', decimal_places=2, max_digits=4)
        large_price = models.DecimalField('Large Price', decimal_places=2, max_digits=4)
        def __str__(self):
            return '{} small: ${} large: ${}'.format(self.item_name, self.small_price, self.large_price)

class Salad(models.Model):
        item_name = models.CharField('Item', max_length=128)
        small_price = models.DecimalField('Small Price', decimal_places=2, max_digits=4)
        large_price = models.DecimalField('Large Price', decimal_places=2, max_digits=4)
        def __str__(self):
            return '{} small: ${} large: ${}'.format(self.item_name, self.small_price, self.large_price)

class Platter(models.Model):
        item_name = models.CharField('Item', max_length=128)
        small_price = models.DecimalField('Small Price', decimal_places=2, max_digits=4)
        large_price = models.DecimalField('Large Price', decimal_places=2, max_digits=4)
        def __str__(self):
            return '{} small: ${} large: ${}'.format(self.item_name, self.small_price, self.large_price)

class Order(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    order_number = models.IntegerField('Order Number:')
    username = models.CharField('Ordered By', max_length=32)
    item = GenericForeignKey('content_type', 'object_id')
    extras = models.CharField('Order Item', max_length=256, default='none')
    date = models.DateField('Order date', auto_now=True)
    completed = models.BooleanField('Completed', default=False)

    def __str__(self):
        return 'Order number:{} was ordered by {} on {}'.format(self.order_number,
            self.username, self.date)

pizza_type = ContentType.objects.get(app_label='orders', model='pizza')
sub_type = ContentType.objects.get(app_label='orders', model='sub')
pasta_type = ContentType.objects.get(app_label='orders', model='pasta')
salad_type = ContentType.objects.get(app_label='orders', model='salad')
platter_type = ContentType.objects.get(app_label='orders', model='platter')