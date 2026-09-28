from django.urls import path
from .views import (
    CheckoutView, OrderListView, OrderDetailView,
    AdminOrderListView, OrderStatusUpdateView,
)

urlpatterns = [
    path('orders/checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/all/', AdminOrderListView.as_view(), name='order-all'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:id>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:id>/status/', OrderStatusUpdateView.as_view(), name='order-status'),
]