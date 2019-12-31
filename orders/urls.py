from django.urls import path

from . import views

urlpatterns = [
    # home and order paths
    path('', views.index_view, name='index'),
    path('order', views.order_view, name='order'),
    path('basket', views.basket_view, name='basket'),
    path('ordered', views.take_order_view, name='ordered'),
    path('my_orders', views.my_orders_view, name='my_orders'),
    path('my_orders/history', views.my_orders_history_view, name='my_orders_history'),
    path('refresh_my_orders', views.refresh_my_orders_view, name='refresh_my_orders'),
    # registration/login paths
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    # staff update and refresh paths
    path('order_list', views.order_list_view, name='order_list'),
    path('refresh_order_list', views.refresh_order_list_view, name='refresh_order_list'),
    path('update_order_list', views.update_order_list_view, name='update_order_list')
]
