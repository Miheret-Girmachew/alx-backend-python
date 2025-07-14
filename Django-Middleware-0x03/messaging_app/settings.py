# Django-Middleware-0x03/messaging_app/settings.py

MIDDLEWARE = [
    # Default Django Middleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', # IMPORTANT: Must come before any middleware that uses request.user
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # --- YOUR CUSTOM MIDDLEWARE IN ORDER OF EXECUTION ---
    
    # 1. First, check if the service is available based on time.
    'chats.middleware.RestrictAccessByTimeMiddleware',
    
    # 2. Next, check if the user has the required role for certain actions.
    'chats.middleware.RolepermissionMiddleware',
    
    # 3. Then, apply rate-limiting to message sending.
    'chats.middleware.OffensiveLanguageMiddleware',
    
    # 4. Finally, if the request is allowed to proceed, log it.
    'chats.middleware.RequestLoggingMiddleware', 
]