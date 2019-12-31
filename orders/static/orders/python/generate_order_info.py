from orders.models import Pizza, Pasta, Platter, Sub, Salad

'''
{'itemType': food type, 'itemSize': size, 'item': food_type databaseID, 'itemNumber': number ordered}
'''

def generate_order_info(order):
    order_list = []
    total_price = 0
    item_count = 0
    for item in order:
        this_item = {
            'item_count': item_count,
            'size': item['itemSize'],
            'number': range(int(item['itemNumber'])),
            'item_type': item['itemType'],
        }
        item_id = item['item'].split(' ')[-1]
        if item['itemType'] == 'Pizza':
            this_item['item_data'] = Pizza.objects.filter(id=item_id)[0]
            this_item['number_of_toppings'] = range(1, Pizza.objects.filter(id=item_id)[0].number_of_toppings + 1)
        if item['itemType'] == 'Pasta':
            this_item['item_data'] = Pasta.objects.filter(id=item_id)[0]
        if item['itemType'] == 'Subs':
            this_item['item_data'] = Sub.objects.filter(id=item_id)[0]
        if item['itemType'] == 'Salad':
            this_item['item_data'] = Salad.objects.filter(id=item_id)[0]
        if item['itemType'] == 'Platter':
            this_item['item_data'] = Platter.objects.filter(id=item_id)[0]
        if this_item['size'] == 'small':
            this_item['price'] = this_item['item_data'].small_price
        else:
            this_item['price'] = this_item['item_data'].large_price
        total_price = total_price + this_item['price']
        order_list.append(this_item)
        item_count += 1
    return [order_list, total_price]

    