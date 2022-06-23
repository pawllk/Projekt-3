import django_filters
from .models import Tournament

class ContestFilter(django_filters.FilterSet):
    class Meta:
        model = Tournament
        fields = '__all__'