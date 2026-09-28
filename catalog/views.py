import django_filters
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Category, Product
from .permissions import IsAdminOrReadOnly
from .serializer import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductWriteSerializer,
)


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method='filter_category')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price']

    def filter_category(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(Q(category_id=value) | Q(category__parent_id=value))
        return queryset.filter(Q(category__slug=value) | Q(category__parent__slug=value))


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.select_related('category')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductWriteSerializer
        return ProductListSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category')
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return ProductWriteSerializer
        return ProductDetailSerializer