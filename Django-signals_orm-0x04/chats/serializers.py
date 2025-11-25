from rest_framework import serializers
from .models import User, Conversation, Message

# User Serializer with CharField and ValidationError
class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'user_id', 'first_name', 'last_name', 'email',
            'phone_number', 'role', 'created_at'
        ]

    def validate_email(self, value):
        if not value.endswith('@example.com'):
            raise serializers.ValidationError("Email must be from @example.com domain.")
        return value

# Message Serializer with nested sender
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id', 'sender', 'message_body',
            'sent_at', 'conversation'
        ]
        read_only_fields = ['sent_at']

# Conversation Serializer with SerializerMethodField
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants',
            'created_at', 'messages'
        ]

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('-sent_at')
        return MessageSerializer(messages, many=True).data