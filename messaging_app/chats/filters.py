import django_filters
from .models import Conversation


class MessageFilter(django_filters.FilterSet):
    class Meta:
        model = Conversation
        fields = {
            "participants_id" : ["exact"],
            "created_at":["range"]
        }
        