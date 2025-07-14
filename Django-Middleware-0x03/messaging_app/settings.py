# Django-Middleware-0x03/messaging_app/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # The order matters. Django processes them from top to bottom.
    
    # 1. First, check if access is allowed based on time.
    #    This runs early to deny access quickly if needed.
    'chats.middleware.RestrictAccessByTimeMiddleware',
    
    # 2. If access is allowed, then log the request.
    #    This ensures even denied requests could be logged if we wanted.
    'chats.middleware.RequestLoggingMiddleware', 
]