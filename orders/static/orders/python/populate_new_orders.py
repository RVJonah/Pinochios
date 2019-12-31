from orders.models import Order

def populate_new_orders(new_order_queryset):
    new_orders = []
    if len(new_order_queryset) != 0:
        for order in new_order_queryset:
            new_order_item = {}
            new_order_item['id'] = order.id
            new_order_item['order_number'] = order.order_number
            new_order_item['username'] = order.username
            new_order_item['item_name'] = order.item.item_name
            new_order_item['item_type'] = str(order.content_type)
            new_order_item['extras'] = order.extras
            new_order_item['date'] = order.date.strftime('%b. %d, %Y')
            new_orders.append(new_order_item)
        return new_orders
    return None