# D:\ALX\alx-backend-python\Django-Middleware-0x03\chats\serializers.py

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model. This tells the Django Rest Framework
    how to convert Message objects into JSON and vice-versa.
    """
    # This adds a read-only field to the API output that shows the sender's username,
    # which is more useful than just the sender's ID number.
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        # These are the fields that will be included in the API response.
        fields = ['id', 'conversation', 'sender', 'sender_username', 'content', 'created_at']
        
        # These fields cannot be set by the user when creating a new message.
        # They are set automatically by the system. The only thing a user provides is 'content'.
        read_only_fields = ['id', 'sender', 'sender_username', 'created_at', 'conversation']