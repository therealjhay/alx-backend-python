import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter by sender email
    sender_email = django_filters.CharFilter(field_name="sender__email", lookup_expr="icontains")
    # Filter by date range
    sent_after = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    sent_before = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")

    class Meta:
        model = Message
        fields = ['sender_email', 'sent_after', 'sent_before']