from django.db.models import Max
from orders.models import pizza_type, pasta_type, sub_type, salad_type, platter_type, Order

def clean_extras_string(extras):
    strings_to_remove = ['=on', 'topping1=', 'topping2=', 'topping3=', 'topping4=', 'topping5=']
    item_extras = extras.split('&')
    item_extras.pop(0)
    cleaned_extras_string = " ".join(item_extras)
    for string in strings_to_remove:
        cleaned_extras_string = cleaned_extras_string.replace(string, '')
    cleaned_extras_string = cleaned_extras_string.replace('%26', '&')
    cleaned_extras_string = cleaned_extras_string.replace(' ', ', ')
    cleaned_extras_string = cleaned_extras_string.replace('%20', ' ')
    return cleaned_extras_string

def complete_order(order, username):
    order_number = Order.objects.aggregate(Max('order_number'))
    if order_number['order_number__max'] == None:
        order_number = 1
    else:
        order_number = order_number['order_number__max'] + 1
    for item in order:
        extras = clean_extras_string(item['extras'])
        item_id = int(item['itemId'])
        item_type = item['itemType'].split(' ')[1]
        if item_type == 'Pizza':
            content_type = pizza_type
        if item_type == 'Subs':
            content_type = sub_type
        if item_type == 'Pasta':
            content_type = pasta_type
        if item_type == 'Salad':
            content_type = salad_type
        if item_type == 'Platter':
            content_type = platter_type
        order_item = Order(
            order_number=order_number,
            username=username,
            object_id=item_id,
            content_type=content_type,
            extras=extras,
            completed=False
            )
        order_item.save()
    return order_number

