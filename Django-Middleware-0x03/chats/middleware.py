import logging
from datetime import datetime

# Configure logger to write to requests.log
logger = logging.getLogger(__name__)
handler = logging.FileHandler("requests.log")   # log file in project root
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware that logs each request with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine user
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        # Continue processing
        response = self.get_response(request)
        return response