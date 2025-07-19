# messaging/models.py

from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    """
    Represents a direct message from one user to another, with support for threading.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Fields to track if a message has been edited
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    # --- NEW FIELD FOR THREADED REPLIES ---
    # This self-referential ForeignKey allows a message to be a reply to another message.
    # 'self' indicates the relationship is with the same model.
    # null=True, blank=True: A message does not have to be a reply.
    # on_delete=models.CASCADE: If a parent message is deleted, all its replies are also deleted.
    # related_name='replies': Allows accessing replies from a parent message instance (e.g., parent.replies.all()).
    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies'
    )

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class MessageHistory(models.Model):
    """
    Stores the history of edits for a single message.
    """
    original_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='edited_messages')
    edited_at = models.DateTimeField()

    def __str__(self):
        return f"Edit for message {self.original_message.id} at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"

class Notification(models.Model):
    """
    Represents a notification for a user about a new message.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} about message from {self.message.sender.username}"