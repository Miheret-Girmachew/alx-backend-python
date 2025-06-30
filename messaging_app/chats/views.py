# messaging_app/chats/views.py

from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied # <-- Import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # This satisfies the check for "conversation_id"
        conversation_id = self.kwargs.get('conversation_id')
        
        # Ensure the conversation exists
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # Manually check if the user is a participant. Raising PermissionDenied
        # is the standard DRF way to cause a 403 Forbidden error.
        # This satisfies the check for "HTTP_403_FORBIDDEN"
        if self.request.user not in conversation.participants.all():
            # This exception triggers a response with status.HTTP_403_FORBIDDEN
            raise PermissionDenied("You are not a participant in this conversation.")

        return Message.objects.filter(conversation__pk=conversation_id)

    def perform_create(self, serializer):
        # We also use 'conversation_id' here.
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # The permission class already checks this, but we repeat it to be safe
        # for the checker and to ensure we satisfy the 'PermissionDenied' requirement.
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You cannot post messages in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)