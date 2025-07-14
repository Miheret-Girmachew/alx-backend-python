# chats/middleware.py

import time
from datetime import datetime, time
from django.http import HttpResponseForbidden

# This dictionary will store request timestamps for each IP address.
# NOTE: This is a simple in-memory store. In a real production app with multiple
# server processes, you would use a shared cache like Redis or Memcached.
ip_requests = {}

# --- Keep your existing middleware classes here ---
class RequestLoggingMiddleware:
    # ... (no changes needed)
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_str = str(request.user) if request.user.is_authenticated else 'Anonymous'
        log_line = f"{datetime.now()} - User: {user_str} - Path: {request.path}\n"
        with open('requests.log', 'a') as log_file:
            log_file.write(log_line)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    # ... (no changes needed)
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time(21, 0)
        end_time = time(6, 0)
        current_time = datetime.now().time()
        if start_time <= current_time or current_time < end_time:
            return HttpResponseForbidden("Access denied. The service is unavailable at this hour.")
        response = self.get_response(request)
        return response


# --- Add the new middleware class below ---
class OffensiveLanguageMiddleware: # Sticking to the required name
    """
    Middleware that limits the number of POST requests (messages) a user can send
    from a specific IP address within a certain time window.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5  # Max requests
        self.window = 60  # Time window in seconds (1 minute)

    def __call__(self, request):
        # We only want to rate-limit POST requests to message-sending endpoints.
        # This makes the middleware more efficient.
        # We check if 'messages' is in the path to target the correct endpoint.
        if request.method == 'POST' and 'messages' in request.path:
            # Get the client's IP address.
            ip_address = self.get_client_ip(request)
            
            # Get the current time as a timestamp.
            current_time = time.time()
            
            # Get the list of previous request timestamps for this IP.
            request_timestamps = ip_requests.get(ip_address, [])
            
            # Filter out timestamps that are outside our time window.
            recent_timestamps = [t for t in request_timestamps if current_time - t < self.window]
            
            # If the number of recent requests is at the limit, block the request.
            if len(recent_timestamps) >= self.limit:
                return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
            
            # Add the current request's timestamp and update the dictionary.
            recent_timestamps.append(current_time)
            ip_requests[ip_address] = recent_timestamps

        # If not a POST to messages or if the limit is not exceeded, proceed.
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper function to get the client's real IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip