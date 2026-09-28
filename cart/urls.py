from django.urls import path
from .views import (
    CartView, AddToCartView, CartItemDetailView, ClearCartView, RemoveFromCartView
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='cart-add'),
    path('cart/remove/', RemoveFromCartView.as_view(), name='cart-remove'),
    path('cart/items/<int:id>/', CartItemDetailView.as_view(), name='cart-item'),
    path('cart/clear/', ClearCartView.as_view(), name='cart-clear'),
]