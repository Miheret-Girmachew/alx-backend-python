
import time
from datetime import datetime, time
from django.http import HttpResponseForbidden

ip_requests = {}


class RequestLoggingMiddleware:
    """
    Logs each user's request to a file.
    """
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
    """
    Restricts access to the site between 9 PM and 6 AM.
    """
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


class OffensiveLanguageMiddleware:
    """
    Limits the number of POST requests (messages) from an IP address.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.limit = 5  # Max requests per window
        self.window = 60  # Window size in seconds (1 minute)

    def __call__(self, request):
        # We only apply the limit to POST requests to message endpoints.
        if request.method == 'POST' and 'messages' in request.path:
            ip_address = self.get_client_ip(request)
            current_time = time.time()
            
            request_timestamps = ip_requests.get(ip_address, [])
            
            # Remove timestamps that are older than our window.
            recent_timestamps = [t for t in request_timestamps if current_time - t < self.window]
            
            if len(recent_timestamps) >= self.limit:
                return HttpResponseForbidden("Rate limit exceeded. Please try again later.")
            
            recent_timestamps.append(current_time)
            ip_requests[ip_address] = recent_timestamps

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper function to get the client's IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip