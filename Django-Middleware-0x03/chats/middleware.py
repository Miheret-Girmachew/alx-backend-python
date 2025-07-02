# Django-Middleware-0x03/chats/middleware.py

import logging
from datetime import datetime

# Set up a basic logger that writes to a file named 'requests.log'
# This will create the file in your project's root directory.
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(message)s'  # Log only the message we provide
)

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
        # Get the user. If the user is not authenticated, it will be an 'AnonymousUser'.
        # We use str() to get a clean string representation for both cases.
        user = str(request.user)
        
        # This is the exact log format required by the instructions.
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        
        # Use the configured logger to write the message to the file.
        logging.info(log_message)

        # This passes the request to the next middleware or to the view.
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        # We don't need any for this task.

        return response