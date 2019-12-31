import json
from orders.models import Order

def mark_completed_orders(orders):
    parsed_orders = json.loads(orders)
    for id_number in parsed_orders:
        order = Order.objects.filter(id=id_number)[0]
        order.completed = True
        order.save()