# D:\ALX\alx-backend-python\Django-Middleware-0x03\messaging_app\urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This line tells the project to look in chats/urls.py for any URL starting with 'api/'
    path('api/', include('chats.urls')), 

    # URLs for getting a JWT token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]