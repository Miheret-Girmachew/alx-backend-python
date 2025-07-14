# chats/middleware.py

import logging
from datetime import datetime

# Get the logger we will configure in settings.py
logger = logging.getLogger('request_logger')

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view is called.
        """
        # Get user information. If not logged in, it will be an AnonymousUser.
        user = request.user if request.user.is_authenticated else 'Anonymous'
        
        # Format the log message as required
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        
        # Log the message using our configured logger
        logger.info(log_message)

        # Pass the request to the next middleware or view
        response = self.get_response(request)

        # Code to be executed for each response after the view is called (optional)

        return response