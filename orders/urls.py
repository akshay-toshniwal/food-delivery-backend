from django.urls import path
from .views import CreateOrderAPIView, UserOrderListView

urlpatterns = [
    path('order/orders/list', UserOrderListView.as_view(), name='orders'),
    path('order/create-order', CreateOrderAPIView.as_view(), name='create-order'),
]
