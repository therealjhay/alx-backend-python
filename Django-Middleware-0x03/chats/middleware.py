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
    Middleware that logs each request with timestamp, user, method, path, and response status.
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
    Middleware that restricts access to the messaging app
    outside of 6 AM - 9 PM server time.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        current_hour = datetime.now().hour

        # Allowed hours: 6 <= hour < 21
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
    Middleware that limits the number of chat messages a user can send
    within a certain time window, based on their IP address.
    - Max: 5 messages per minute per IP
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = defaultdict(list)
        self.limit = 5          # max messages
        self.time_window = 60   # seconds (1 minute)

    def __call__(self, request: HttpRequest):
        # Only enforce on POST requests to /messages/
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean up old timestamps outside the time window
            self.ip_requests[ip] = [
                ts for ts in self.ip_requests[ip] if now - ts < self.time_window
            ]

            # Check if limit exceeded
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

            # Record this request timestamp
            self.ip_requests[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request: HttpRequest):
        """Helper to extract client IP address"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip