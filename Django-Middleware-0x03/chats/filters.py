# messaging_app/chats/filters.py

import django_filters
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    """
    FilterSet for the Message model.
    Allows filtering by sender and by a created_at time range.
    """
    # Filter to find messages sent by a specific user (using their username)
    sender = django_filters.ModelChoiceFilter(
        field_name='sender__username',
        to_field_name='username',
        queryset=User.objects.all(),
        label='Sender Username'
    )

    # Filter for messages created AFTER a certain datetime (e.g., ?start_date=2024-01-01T00:00:00Z)
    start_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')

    # Filter for messages created BEFORE a certain datetime (e.g., ?end_date=2024-01-31T23:59:59Z)
    end_date = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'start_date', 'end_date']