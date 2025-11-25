from django.contrib.auth import get_user_model, logout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

User = get_user_model()


@login_required
@require_POST
def delete_user(request):
    """
    View that allows a logged-in user to delete their account.
    """
    user = request.user

    # Log out the user before deletion
    logout(request)

    # Delete the user (signals will handle cleanup)
    user.delete()

    return JsonResponse({"message": "Your account and related data have been deleted."})