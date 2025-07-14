from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')

    def test_notification_is_created_on_new_message(self):
        """
        Tests that a Notification is automatically created when a new Message is saved.
        """
        # Check that there are no notifications initially.
        self.assertEqual(Notification.objects.count(), 0)
        
        # Create a new message from user1 to user2.
        Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello from a test!"
        )
        
        # Assert that one notification has been created.
        self.assertEqual(Notification.objects.count(), 1)
        
        # Assert that the notification belongs to the correct user (the receiver).
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.user2)