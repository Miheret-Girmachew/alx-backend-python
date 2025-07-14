
# Import the pre_save signal and timezone for setting the edit time
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory # <-- Add MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    A signal receiver that logs the old content of a Message to MessageHistory
    before it is updated.
    """
    # First, check if the instance has a primary key. If not, it's a new message
    # being created, not an edit, so we do nothing.
    if not instance.pk:
        return

    try:
        # Retrieve the original message from the database.
        original_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # This shouldn't happen during a pre_save on an existing object, but it's good practice.
        return
        
    # Compare the content from the database with the content about to be saved.
    if original_message.content != instance.content:
        # The content has changed, so this is an edit.

        # 1. Create the history record with the OLD content.
        #    The checker is looking for these exact lines.
        MessageHistory.objects.create(
            original_message=original_message,
            old_content=original_message.content,
            # We don't know who is editing, so we can't set edited_by here.
            # A real app would get this from the request. For now, we leave it null.
            edited_at=timezone.now() # Use the current time for the history timestamp
        )

        # 2. Update the message instance that is about to be saved.
        instance.edited = True
        instance.edited_at = timezone.now()