from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    """

    def for_user(self, user):
        # ✅ Filter unread messages for the given user
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")  # optimization
        )


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ New field to track read/unread status
    read = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        "self",
        related_name="replies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The message this one is replying to"
    )

    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        related_name="edited_messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # ✅ Attach custom manager
    objects = models.Manager()              # default manager
    unread = UnreadMessagesManager()        # custom manager

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"