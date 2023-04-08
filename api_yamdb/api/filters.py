from django_filters import CharFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['name', 'category', 'genre', 'year']
