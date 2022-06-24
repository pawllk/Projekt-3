import django_filters
from .models import Tournament

class ContestFilter(django_filters.FilterSet):
    
    start_date = django_filters.DateFilter(field_name="date", lookup_expr="gte", label="Data od:")
    end_date = django_filters.DateFilter(field_name="date", lookup_expr="lte", label="Data do:")
    start_time = django_filters.DateFilter(field_name="time", lookup_expr="gte", label="Czas od:")
    end_time = django_filters.DateFilter(field_name="time", lookup_expr="lte", label="Czas do:")
    
    class Meta:
        model = Tournament
        fields = []
        exclude = ['status', 'phase', 'player', 'date', 'time']