
from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to interact with it.
    This covers sending, viewing, updating, and deleting messages.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant of the conversation related to the object.
        'obj' can be a Conversation or a Message instance.
        """

        if obj.__class__.__name__ == 'Conversation':
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False

    def has_permission(self, request, view):
        """
        Check if the user can send a message to the specified conversation.
        """

        if request.method == 'POST':
            conversation_pk = view.kwargs.get('conversation_pk')
            if not conversation_pk:
                return False

            from .models import Conversation
            try:
                conversation = Conversation.objects.get(pk=conversation_pk)
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False
        

        return True