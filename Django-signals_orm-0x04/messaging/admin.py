from django.contrib import admin
from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "content", "timestamp")
    list_filter = ("sender", "receiver", "timestamp")
    search_fields = ("content",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "message", "created_at", "is_read")
    list_filter = ("user", "is_read", "created_at")
    search_fields = ("message__content",)