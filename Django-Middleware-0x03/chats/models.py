# D:\ALX\alx-backend-python\Django-Middleware-0x03\chats\models.py

from django.db import models
from django.contrib.auth import get_user_model

# Get the standard User model from Django
User = get_user_model()

class Conversation(models.Model):
    """
    Represents a conversation between two or more users.
    """
    # The 'participants' field is a many-to-many relationship with the User model.
    # A user can be in many conversations, and a conversation can have many users.
    # The `related_name` 'conversations' lets us do `user.conversations.all()`
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    # The 'sender' is a foreign key to the User model. If a User is deleted,
    # their messages are also deleted (CASCADE).
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # The 'conversation' is a foreign key to the Conversation model.
    # This links the message to a specific conversation.
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    
    # The actual text content of the message.
    content = models.TextField()
    
    # Timestamps for creation and last update.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"