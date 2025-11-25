from django.contrib import admin
from .models import Message, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "receiver", "content", "timestamp", "edited")
    list_filter = ("sender", "receiver", "edited")
    search_fields = ("content",)


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "message", "old_content", "edited_at")
    list_filter = ("edited_at",)
    search_fields = ("old_content",)