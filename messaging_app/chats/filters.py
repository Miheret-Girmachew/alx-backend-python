
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for the Message model.
    Allows filtering messages by a start and end date.
    """
    # 'gte' stands for 'greater than or equal to'
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    # 'lte' stands for 'less than or equal to'
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')

    class Meta:
        model = Message
        # The fields we can filter on.
        fields = ['start_date', 'end_date']