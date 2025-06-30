from rest_framework import permissions

class IsParticipantInConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to see it.
    """

    def has_object_permission(self, request, view, obj):
      
        return request.user in obj.participants.all()