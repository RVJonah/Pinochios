import json

def get_order_items(cookie):
    order_string_list = cookie.split("-")
    order_items = list(map(json.loads, order_string_list))
    return order_items