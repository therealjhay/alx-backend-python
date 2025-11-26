from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ Self-referential foreign key for threaded replies
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

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"

    # ✅ Recursive method to fetch replies in threaded format
    def get_thread(self):
        """
        Recursively fetch all replies to this message.
        Returns a list of dicts with nested replies.
        """
        thread = []
        # Optimize queries: select_related for FK, prefetch_related for reverse FK
        replies_qs = self.replies.all().select_related("sender", "receiver").prefetch_related("replies")
        for reply in replies_qs:
            thread.append({
                "id": reply.id,
                "sender": reply.sender.username,
                "receiver": reply.receiver.username,
                "content": reply.content,
                "timestamp": reply.timestamp,
                "replies": reply.get_thread()  # recursion
            })
        return thread