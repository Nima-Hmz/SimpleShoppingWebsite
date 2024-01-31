from django.urls import path
from .views import CartView,CartAddView, CartRemoveView, OrderCreateView, OrderDetailView, OrderPayView, OrderVertifyView

app_name = "shop_orders"

urlpatterns = [

    path("cart/", CartView.as_view(), name="cart"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("detail/<int:order_id>/", OrderDetailView.as_view(), name="order_detail"),
    path("cart/add/<int:product_id>/", CartAddView.as_view(), name="cart_add"),
    path('cart/remove/<int:product_id>', CartRemoveView.as_view(), name='cart_remove'),
    path("pay/<int:order_id>/", OrderPayView.as_view(), name="order_pay"),
    path("vertify/", OrderVertifyView.as_view(), name="order_vertify")
]   