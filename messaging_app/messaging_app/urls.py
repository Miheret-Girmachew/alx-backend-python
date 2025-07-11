# messaging_app/messaging_app/urls.py

from django.contrib import admin
from django.urls import path, include
# Import the views provided by simplejwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your app's API endpoints
    path('api/', include('chats.urls')),
    
    # DRF login/logout views for the Browsable API
    path('api-auth/', include('rest_framework.urls')),

    # JWT Token Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]