from django.forms import DateInput
from django_filters import FilterSet, DateFilter, ModelChoiceFilter, CharFilter
from .models import Author


class PostFilter(FilterSet):

    title = CharFilter(
        label='Заголовок',
        lookup_expr='iregex'
    )

    author = ModelChoiceFilter(
        empty_label='Все авторы',
        label='Автор',
        queryset=Author.objects.all()
    )

    created_at = DateFilter(
        field_name='created_at',
        widget=DateInput(attrs={'type': 'date'}),
        lookup_expr='date__gte',
        label='Дата'
    )
