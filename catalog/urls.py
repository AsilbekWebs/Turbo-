from django.urls import path
from .views import (
    CategoryListCreateView, CategoryDetailView,
    ProductListCreateView, ProductDetailView,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
]