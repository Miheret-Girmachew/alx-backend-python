# messaging_app/settings.py

# ... (other settings like INSTALLED_APPS should already be here) ...

# 1. Add your custom middleware to the MIDDLEWARE list.
# The order can be important. Placing it here is generally safe.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'chats.middleware.RequestLoggingMiddleware', # <-- ADD THIS LINE
]

# ... (other settings like ROOT_URLCONF, TEMPLATES, DATABASES) ...

# 2. Add the LOGGING configuration at the bottom of the file.
# This tells Django how to handle the logger we used in our middleware.
import os # Make sure 'os' is imported at the top of your settings.py
from pathlib import Path # Make sure 'pathlib' is imported as well for BASE_DIR

# Assuming BASE_DIR is defined as: BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'request_log_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            # This will create the requests.log file in your project's root directory
            'filename': os.path.join(BASE_DIR, 'requests.log'),
            'formatter': 'simple',
        },
    },
    'loggers': {
        'request_logger': { # This is the name we used in middleware.py
            'handlers': ['request_log_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'formatters': {
        'simple': {
            'format': '{message}',
            'style': '{',
        },
    },
}