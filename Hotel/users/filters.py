import django_filters
from .models import CustomUser

class UserFilter(django_filters.FilterSet):

    CHOICES = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending')
    )

    ordering = django_filters.ChoiceFilter(label='Ordering', choices=CHOICES, method='filter_by_order')

    class Meta:
        model = CustomUser
        fields = {
            'email': ['icontains'],
        }

    def filter_by_order(self, queryset, name, value):
        expression = 'email' if value == 'ascending' else '-email'
        return queryset.order_by(expression)    