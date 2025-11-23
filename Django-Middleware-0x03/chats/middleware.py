import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# Configure logger to write to requests.log
logger = logging.getLogger("request_logger")

if not logger.handlers:
    handler = logging.FileHandler("requests.log")   # log file in project root
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """
    Middleware that logs each request with timestamp, user, method, path, and response status.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        response = self.get_response(request)

        log_message = (
            f"{datetime.now()} - User: {user} - Method: {request.method} "
            f"- Path: {request.path} - Status: {response.status_code}"
        )
        logger.info(log_message)

        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app
    outside of 6 AM - 9 PM server time.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour

        # Allowed hours: 6 <= hour < 21
        if current_hour < 6 or current_hour >= 21:
            # Log the blocked attempt
            user = request.user if request.user.is_authenticated else "Anonymous"
            log_message = (
                f"{datetime.now()} - User: {user} - Method: {request.method} "
                f"- Path: {request.path} - Status: 403 (Blocked by time restriction)"
            )
            logger.info(log_message)

            return HttpResponseForbidden(
                "Access to the messaging app is restricted between 9 PM and 6 AM."
            )

        return self.get_response(request)