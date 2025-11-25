from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessagingSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="pass123")
        self.receiver = User.objects.create_user(username="receiver", password="pass123")

    def test_notification_created_on_message(self):
        # Send a message
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello, this is a test message."
        )

        # Check that a notification was created
        notif = Notification.objects.filter(user=self.receiver, message=msg).first()
        self.assertIsNotNone(notif)
        self.assertFalse(notif.is_read)