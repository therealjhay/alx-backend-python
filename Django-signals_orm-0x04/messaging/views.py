from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

from .models import Message, User


@csrf_exempt
@login_required
@require_POST
def send_message(request):
    """
    View to send a new message.
    Automatically sets sender=request.user and requires a receiver.
    """
    receiver_id = request.POST.get("receiver")
    content = request.POST.get("content")

    if not receiver_id or not content:
        return JsonResponse({"error": "Receiver and content are required."}, status=400)

    receiver = get_object_or_404(User, pk=receiver_id)

    # ✅ sender=request.user, receiver=receiver
    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )

    return JsonResponse({
        "id": message.id,
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "timestamp": message.timestamp
    })


@login_required
def conversation_view(request, user_id):
    """
    Retrieve all messages between the logged-in user and another user.
    Optimized with select_related and prefetch_related.
    """
    other_user = get_object_or_404(User, pk=user_id)

    # ✅ Use Message.objects.filter with select_related
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