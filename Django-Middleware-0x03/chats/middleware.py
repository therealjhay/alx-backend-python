import logging
import time
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseForbidden, HttpRequest

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
    Logs each request with timestamp, user, method, path, and response status.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
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
    Restricts access outside of 6 AM - 9 PM server time.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        current_hour = datetime.now().hour

        if current_hour < 6 or current_hour >= 21:
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


class OffensiveLanguageMiddleware:
    """
    Limits number of chat messages a user can send per IP.
    Max: 5 POST requests to /messages/ per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = defaultdict(list)
        self.limit = 5
        self.time_window = 60  # seconds (1 minute)

    def __call__(self, request: HttpRequest):
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean up old timestamps
            self.ip_requests[ip] = [
                ts for ts in self.ip_requests[ip] if now - ts < self.time_window
            ]

            if len(self.ip_requests[ip]) >= self.limit:
                user = request.user if request.user.is_authenticated else "Anonymous"
                log_message = (
                    f"{datetime.now()} - User: {user} - IP: {ip} - Method: {request.method} "
                    f"- Path: {request.path} - Status: 403 (Rate limit exceeded)"
                )
                logger.info(log_message)

                return HttpResponseForbidden(
                    "You have exceeded the limit of 5 messages per minute. Please wait before sending more."
                )

            self.ip_requests[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request: HttpRequest):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class RolepermissionMiddleware:
    """
    Restricts access to certain actions based on user role.
    Only 'admin' or 'moderator' are allowed.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        user = request.user

        if user.is_authenticated:
            role = getattr(user, "role", None)

            if role not in ["admin", "moderator"]:
                log_message = (
                    f"{datetime.now()} - User: {user} - Method: {request.method} "
                    f"- Path: {request.path} - Status: 403 (Role restriction)"
                )
                logger.info(log_message)

                return HttpResponseForbidden(
                    "You do not have permission to perform this action."
                )

        return self.get_response(request)