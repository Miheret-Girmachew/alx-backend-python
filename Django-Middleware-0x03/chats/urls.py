# D:\ALX\alx-backend-python\Django-Middleware-0x03\chats\urls.py

from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
# The 'r' prefix means "raw string" and is good practice for regex
router.register(r'conversations', ConversationViewSet, basename='conversation')

# This creates nested routes like /conversations/{conversation_pk}/messages/
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]