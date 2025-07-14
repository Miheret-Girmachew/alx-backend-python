from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    A signal receiver that creates a Notification whenever a new Message is created.
    """
    # The 'created' boolean is True only if a new record was created.
    # This prevents creating notifications when a message is updated.
    if created:
        # The 'instance' is the Message object that was just saved.
        message = instance
        
        # Create a new Notification for the receiver of the message.
        Notification.objects.create(
            user=message.receiver,
            message=message
        )
        
        # Optional: print a confirmation to the console for debugging
        print(f"Notification created for user '{message.receiver.username}' for message ID {message.id}")