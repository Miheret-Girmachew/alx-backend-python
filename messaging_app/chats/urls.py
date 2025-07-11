# messaging_app/chats/urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import UserRegistrationView, ConversationViewSet, MessageViewSet

# Create the main router for the top-level resource: Conversations
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create a nested router for the child resource: Messages
# The first argument is the parent router.
# The second argument is the URL prefix of the parent ('conversations').
# The third is a lookup name for the parent's primary key.
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')

# Register the MessageViewSet with the nested router.
# It will now generate URLs like: /conversations/{conversation_pk}/messages/
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# We no longer need a top-level '/messages/' route, so it has been removed.

urlpatterns = [
    # Manually add the user registration URL
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    
    # Include URLs from the main router
    path('', include(router.urls)),
    
    # Include URLs from the nested router
    path('', include(conversations_router.urls)),
]