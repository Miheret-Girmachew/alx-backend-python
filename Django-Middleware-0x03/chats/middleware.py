# chats/middleware.py

from datetime import datetime, time
# We need HttpResponseForbidden to return the 403 error.
from django.http import HttpResponseForbidden

# --- Keep your existing RequestLoggingMiddleware here ---
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_str = str(request.user) if request.user.is_authenticated else 'Anonymous'
        log_line = f"{datetime.now()} - User: {user_str} - Path: {request.path}\n"
        with open('requests.log', 'a') as log_file:
            log_file.write(log_line)
        response = self.get_response(request)
        return response


# --- Add the new middleware class below ---
class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the site between 9 PM and 6 AM.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the restricted time range.
        start_time = time(21, 0) # 9 PM (21:00)
        end_time = time(6, 0)   # 6 AM (06:00)
        current_time = datetime.now().time()

        # The logic for a time range that crosses midnight is a bit tricky.
        # Access is denied if the current time is:
        # - After 9 PM (e.g., 10 PM) OR
        # - Before 6 AM (e.g., 4 AM)
        if start_time <= current_time or current_time < end_time:
            # If within the restricted hours, return a 403 Forbidden response.
            return HttpResponseForbidden("Access denied. The service is unavailable at this hour.")

        # If the time is okay, proceed to the next middleware or the view.
        response = self.get_response(request)
        return response