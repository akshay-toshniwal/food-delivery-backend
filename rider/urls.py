from django.urls import path
from .views import RiderUpdateLocationView, RiderProfileUpdateView, RiderUpdateOrderView, RiderDeliveredOrdersView

urlpatterns = [
    path('rider/update/profile', RiderProfileUpdateView.as_view(), name='update-rider-profile'),
    path('rider/update/location', RiderUpdateLocationView.as_view(), name='update-rider-location'),
    path('rider/update/order', RiderUpdateOrderView.as_view(), name='update-rider-order'),
    path('rider/delivered/orders', RiderDeliveredOrdersView.as_view(), name='rider-delivered-orders'),
]
