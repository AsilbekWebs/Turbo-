import django_filters
from django.db.models import Q
from .models import Product


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