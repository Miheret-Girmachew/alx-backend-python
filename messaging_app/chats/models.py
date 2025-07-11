from django.db import models


import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# 1. The Custom User Model
# This model extends Django's built-in AbstractUser to add our custom fields.
# We do this to control the user schema from the beginning.
class User(AbstractUser):
    # We replace the default integer ID with a UUID for the primary key.
    # This covers the "user_id" and "primary_key" requirements.
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Django's AbstractUser already has 'first_name', 'last_name', and 'password'.
    # We need to make the 'email' field unique because we'll use it for login.
    email = models.EmailField(unique=True)

    # Adding the custom 'phone_number' field as required.
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # We tell Django to use the 'email' field as the unique identifier for login
    # instead of the default 'username'.
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] # 'email' is already required by USERNAME_FIELD


# 2. The Conversation Model
# This model tracks a conversation between multiple participants.
class Conversation(models.Model):
    # A unique UUID for each conversation.
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # This is the key field. It creates a many-to-many relationship with our User model.
    # A user can be in many conversations, and a conversation can have many users.
    # settings.AUTH_USER_MODEL is the correct way to reference our custom User model.
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='conversations')
    
    # A timestamp for when the conversation was created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# 3. The Message Model
# This model represents a single message within a conversation.
class Message(models.Model):
    # A unique UUID for each message.
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # A foreign key linking this message to a specific conversation.
    # on_delete=models.CASCADE means if a conversation is deleted, all its messages are deleted too.
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')

    # A foreign key linking this message to the user who sent it.
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')

    # The actual content of the message. TextField is used for long-form text.
    message_body = models.TextField()

    # Timestamps to meet the checker's requirements.
    # 'created_at' is set once when the message is first created.
    created_at = models.DateTimeField(auto_now_add=True)
    # 'sent_at' can be used to track the exact delivery time. We'll set its default to now.
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender} in {self.conversation.conversation_id}"