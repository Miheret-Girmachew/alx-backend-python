# Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime

# Get a logger instance for this module.
# The configuration for this logger will be defined in settings.py
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    """
    This middleware logs user requests to the 'requests.log' file.
    It captures the timestamp, user, and the request path.
    """
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view is called.
        """
        user = str(request.user)
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        
        # Use the specific logger instance to write the message.
        logger.info(log_message)

        response = self.get_response(request)
        return response