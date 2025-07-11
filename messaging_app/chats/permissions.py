# messaging_app/chats/permissions.py

from rest_framework import permissions
from .models import Conversation

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it
    and its related objects (like messages).
    """

    def has_permission(self, request, view):
        """
        Check for permissions that don't depend on a specific object instance,
        like creating a message.
        """
        # This check is for creating a new message (POST on MessageViewSet).
        if view.basename == 'conversation-messages' and request.method == 'POST':
            # Get the conversation_id from the URL kwargs provided by the nested router.
            conversation_pk = view.kwargs.get('conversation_pk')
            if not conversation_pk:
                return False
            
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
                # Allow access if the user is a participant in the conversation.
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False
        
        # For other actions (like listing conversations), the view's get_queryset
        # already filters by user, so we can allow access here.
        return True

    def has_object_permission(self, request, view, obj):
        """
        Check for permissions that do depend on a specific object instance,
        like retrieving, updating, or deleting a conversation.
        """
        # The 'obj' here is the Conversation instance for ConversationViewSet.
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        
        # If the object is a Message, check the message's conversation.
        # This is a good defensive check, though our URL structure already helps.
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False