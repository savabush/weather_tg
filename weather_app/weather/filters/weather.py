import django_filters

from weather.models import Coordinate


class WeatherFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(lookup_expr='icontains', field_name='name')

    class Meta:
        model = Coordinate
        fields = ('city',)
