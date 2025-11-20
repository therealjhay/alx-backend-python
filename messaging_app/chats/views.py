from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # ✅ Only return conversations where the logged-in user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response({"error": "Participants are required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)
        # ✅ Ensure the creator is also added as a participant
        conversation.participants.add(request.user)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__email']
    ordering_fields = ['sent_at']

    def get_queryset(self):
        # ✅ Only return messages from conversations the logged-in user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not all([conversation_id, message_body]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        # ✅ Ensure the user is part of the conversation before sending a message
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)