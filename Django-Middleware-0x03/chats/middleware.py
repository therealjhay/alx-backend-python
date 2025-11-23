import logging
from datetime import datetime
from django.http import HttpRequest

# Configure logger to write to requests.log
logger = logging.getLogger("request_logger")

# Prevent duplicate handlers if middleware reloads
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

    def __call__(self, request: HttpRequest):
        # Determine user
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Process request and get response
        response = self.get_response(request)

        # Log the request details
        log_message = (
            f"{datetime.now()} - User: {user} - Method: {request.method} "
            f"- Path: {request.path} - Status: {response.status_code}"
        )
        logger.info(log_message)

        return response