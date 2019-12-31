import json
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from orders.models import Order

def send_completion_emails(orders):
  parsed_orders = json.loads(orders)
  orders_updated = []
  user = None
  for order_id in parsed_orders:
      order_number = Order.objects.filter(id=order_id)[0].order_number
      if order_number not in orders_updated:
        orders_updated.append(order_number)
  for order in orders_updated:
      order_complete = True
      items_to_check_for_completion = Order.objects.filter(order_number=order)
      username = items_to_check_for_completion[0].username
      user = User.objects.filter(username=username)[0]
      for item in items_to_check_for_completion:
        if item.completed == False:
          order_complete = False
      if order_complete:
          send_mail(
            subject="Pinochio Order Complete",
            message="Your order number {} is now ready for collection. Thank you for your order".format(order),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=True
            )
  return