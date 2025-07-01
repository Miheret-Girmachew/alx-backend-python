# messaging_app/chats/permissions.py

from rest_framework import permissions
from .models import Conversation, Message

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission that checks:
    1. If the user is authenticated.
    2. If the user is a participant of the conversation for any request method.
    """

    def _is_participant(self, user, conversation):
        """Helper method to check for participation."""
        return user in conversation.participants.all()

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == 'POST':
            conversation_id = view.kwargs.get('conversation_id')
            if not conversation_id:
                return False
            
            try:
                conversation = Conversation.objects.get(pk=conversation_id)
                return self._is_participant(request.user, conversation)
            except Conversation.DoesNotExist:
                return False
        
        return True

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        edit_methods = ["PUT", "PATCH", "DELETE"]

        conversation = None
        if isinstance(obj, Message):
            conversation = obj.conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        
        if not conversation:
            return False

        return self._is_participant(request.user, conversation)