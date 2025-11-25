from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()


@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Automatically delete all related messages, notifications,
    and message histories when a user account is deleted.
    """
    # Delete messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications belonging to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories where user was editor
    MessageHistory.objects.filter(edited_by=instance).delete()