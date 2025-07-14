# messaging_app/settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # --- YOUR CUSTOM MIDDLEWARE ---
    
    # 1. Check time-based access.
    'chats.middleware.RestrictAccessByTimeMiddleware',
    
    # 2. Check rate-limiting for message sending.
    'chats.middleware.OffensiveLanguageMiddleware',
    
    # 3. Log the request if it passed all checks.
    'chats.middleware.RequestLoggingMiddleware', 
]