# Django-Middleware-0x03/messaging_app/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # --- YOUR CUSTOM MIDDLEWARE IN ORDER ---
    
    # 1. First, restrict access by time.
    'chats.middleware.RestrictAccessByTimeMiddleware',
    
    # 2. Next, check for rate-limiting.
    'chats.middleware.OffensiveLanguageMiddleware',
    
    # 3. Finally, if the request is allowed, log it.
    'chats.middleware.RequestLoggingMiddleware', 
]