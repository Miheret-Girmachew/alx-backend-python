
from django.db import models
from django.contrib.auth.models import User
# --- IMPORT THE MANAGER FROM ITS NEW FILE ---
from .managers import UnreadMessagesManager



class Message(models.Model):
    """
    Represents a direct message from one user to another, with support for threading.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    parent_message = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies'
    )
    # The new 'read' field for this task.
    read = models.BooleanField(default=False)

    # Attach the managers to the model.
    objects = models.Manager()  # The default manager.
    unread = UnreadMessagesManager()  # Our custom manager.

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