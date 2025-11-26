from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout

from .models import Message, User


@csrf_exempt
@login_required
@require_POST
def send_message(request):
    """
    Send a new message.
    Automatically sets sender=request.user and requires a receiver.
    Supports replying to a parent_message for threaded conversations.
    """
    receiver_id = request.POST.get("receiver")
    content = request.POST.get("content")
    parent_id = request.POST.get("parent_message")

    if not receiver_id or not content:
        return JsonResponse({"error": "Receiver and content are required."}, status=400)

    receiver = get_object_or_404(User, pk=receiver_id)
    parent_message = None
    if parent_id:
        parent_message = get_object_or_404(Message, pk=parent_id)

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent_message
    )

    return JsonResponse({
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp,
        "parent_message": message.parent_message.id if message.parent_message else None
    })


@login_required
def conversation_view(request, user_id):
    """
    Retrieve all messages between the logged-in user and another user.
    Optimized with select_related and prefetch_related.
    """
    other_user = get_object_or_404(User, pk=user_id)

    messages = (
        Message.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user],
            parent_message__isnull=True  # top-level messages only
        )
        .select_related("sender", "receiver")
        .prefetch_related("replies__sender", "replies__receiver")
        .order_by("timestamp")
    )

    data = []
    for msg in messages:
        data.append({
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "thread": msg.get_thread()  # recursive threaded replies
        })

    return JsonResponse(data, safe=False)


@login_required
def unread_inbox(request):
    """
    Display only unread messages for the logged-in user.
    Uses the custom manager: Message.unread.unread_for_user(request.user).
    """
    unread_messages = Message.unread.unread_for_user(request.user)

    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in unread_messages
    ]

    return JsonResponse(data, safe=False)


@login_required
@require_POST
def delete_user(request):
    """
    Allow a logged-in user to delete their account.
    Signals handle cleanup of related data.
    """
    user = request.user
    logout(request)
    user.delete()
    return JsonResponse({"message": "Your account and related data have been deleted."})