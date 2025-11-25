from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, MessageHistory

User = get_user_model()


class MessageEditTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="pass123")
        self.receiver = User.objects.create_user(username="receiver", password="pass123")
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Original content"
        )

    def test_message_edit_creates_history(self):
        # Edit the message
        self.message.content = "Updated content"
        self.message.save()

        # Check that history was created
        history = MessageHistory.objects.filter(message=self.message).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.old_content, "Original content")
        self.assertTrue(self.message.edited)