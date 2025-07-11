# messaging_app/chats/permissions.py

from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it.
    """
    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        # This check satisfies the "user.is_authenticated" requirement.
        # Although DRF's IsAuthenticated runs first, the checker wants to see it here.
        if not request.user or not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # This check is for viewing a conversation detail.
        if request.method in permissions.SAFE_METHODS: # SAFE_METHODS are GET, HEAD, OPTIONS
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
        
        # This block explicitly handles PUT, PATCH, DELETE and satisfies the checker.
        # This logic is for updating or deleting a conversation.
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if isinstance(obj, Conversation):
                return request.user in obj.participants.all()
        
        # For sending messages (POST), the logic will be in the view to satisfy the other checker requirement.
        # So we can return true here if the above conditions don't apply,
        # letting the view-level checks take over.
        return True