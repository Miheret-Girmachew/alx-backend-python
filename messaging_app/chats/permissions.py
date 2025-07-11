from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to view it.
    """
    def has_object_permission(self, request, view, obj):
        # The 'obj' here is the Conversation instance.
        # We check if the requesting user is in the conversation's participants.
        return request.user in obj.participants.all()