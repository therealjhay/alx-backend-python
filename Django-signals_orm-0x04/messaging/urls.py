from django.urls import path
from .views import send_message, conversation_view, unread_inbox, delete_user

urlpatterns = [
    path("send/", send_message, name="send_message"),
    path("conversation/<int:user_id>/", conversation_view, name="conversation_view"),
    path("inbox/unread/", unread_inbox, name="unread_inbox"),
    path("delete-account/", delete_user, name="delete_user"),
]