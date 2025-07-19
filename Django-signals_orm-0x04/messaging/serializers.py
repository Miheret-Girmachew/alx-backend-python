# messaging/serializers.py

from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ReplySerializer(serializers.ModelSerializer):
    # This is a forward declaration for recursion.
    # It will be replaced by the full ThreadedMessageSerializer later.
    replies = serializers.SerializerMethodField()
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'edited', 'replies']

    def get_replies(self, obj):
        # This method will be populated with pre-fetched data.
        if hasattr(obj, 'prefetched_replies'):
            return ThreadedMessageSerializer(obj.prefetched_replies, many=True).data
        return []

class ThreadedMessageSerializer(ReplySerializer):
    # This is the main serializer that inherits from the reply serializer.
    # No extra logic needed here, it's just for clarity and structure.
    pass