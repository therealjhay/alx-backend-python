from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ New fields for edit tracking
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        related_name="edited_messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who last edited this message"
    )

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class MessageHistory(models.Model):
    """
    Stores previous versions of a message when it is edited.
    """
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        related_name="message_edits",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who performed the edit"
    )

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"