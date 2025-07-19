# messaging/serializers.py

from rest_framework import serializers
from .models import Message
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()
    sender = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp', 'edited', 'replies']
    def get_replies(self, obj):
        if hasattr(obj, 'prefetched_replies'):
            return ThreadedMessageSerializer(obj.prefetched_replies, many=True).data
        return []

class ThreadedMessageSerializer(ReplySerializer):
    pass

class UnreadMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender_username', 'content', 'timestamp']