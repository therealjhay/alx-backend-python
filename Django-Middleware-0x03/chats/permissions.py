from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants of a conversation can view, send, update, or delete messages
    """

    def has_permission(self, request, view):
        # ✅ Ensure user is authenticated globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # ✅ Allow safe methods (GET, HEAD, OPTIONS) if user is a participant
        if request.method in permissions.SAFE_METHODS:
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            return False

        # ✅ Explicitly handle unsafe methods: PUT, PATCH, DELETE
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            return False

        # ✅ For POST (creating messages), ensure user is a participant
        if request.method == 'POST':
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            return False

        return False