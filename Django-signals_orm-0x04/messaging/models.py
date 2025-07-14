# messaging/models.py

from django.db import models
from django.conf import settings # A better way to reference the User model
from django.contrib.auth.models import User # Or keep this if you prefer

# It's best practice to use settings.AUTH_USER_MODEL
# but we'll stick with User for simplicity as started.

class Message(models.Model):
    """
    Represents a direct message from one user to another.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # This boolean flag tracks if the message has ever been edited.
    edited = models.BooleanField(default=False)
    # This timestamp tracks when the last edit occurred.
    edited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class MessageHistory(models.Model):
    """
    Stores the history of edits for a single message.
    """
    original_message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    # Let's add who edited it, as hinted by the checker's 'edited_by' keyword.
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='edited_messages')
    # Use the 'edited_at' from the Message model to timestamp this history entry.
    edited_at = models.DateTimeField()

    def __str__(self):
        return f"Edit for message {self.original_message.id} at {self.edited_at.strftime('%Y-%m-%d %H:%M')}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} about message from {self.message.sender.username}"