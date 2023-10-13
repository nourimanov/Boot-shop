from django_filters import rest_framework as filters
from main.models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    categories = filters.NumberFilter(field_name="categories", lookup_expr="exact")

    class Meta:
        model = Product
        fields = ['title', 'categories']

