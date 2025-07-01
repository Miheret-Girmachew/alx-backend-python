# messaging_app/chats/auth.py

from rest_framework import permissions

class IsOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission to only allow:
    - The owner of a message to view it.
    - Participants of a conversation to view it.
    """

    def has_object_permission(self, request, view, obj):
        # The 'obj' can be either a Message or a Conversation instance.
        # We need to handle both cases.

        # Case 1: The object is a Conversation
        # This assumes your Conversation model has a 'participants' field.
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # Case 2: The object is a Message
        # This assumes your Message model has a 'sender' field (or 'user' field).
        if hasattr(obj, 'sender'):
            return obj.sender == request.user

        # Case 3: The object is a Message and we check conversation participants
        # A better approach for messages is to check if the user is part of the message's conversation.
        # This assumes your Message model has a foreign key to Conversation called 'conversation'.
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False