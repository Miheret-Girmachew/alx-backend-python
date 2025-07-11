
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
# The 'conversations' string is the URL prefix for the ConversationViewSet.
router.register(r'conversations', ConversationViewSet, basename='conversation')
# The 'messages' string is the URL prefix for the MessageViewSet.
router.register(r'messages', MessageViewSet, basename='message')

# The API URLs are now determined automatically by the router.
# In addition, we have to manually add the URL for our UserRegistrationView.
urlpatterns = [
    # The URL for user registration
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # The URLs for the ViewSets are included from the router
    path('', include(router.urls)),
]