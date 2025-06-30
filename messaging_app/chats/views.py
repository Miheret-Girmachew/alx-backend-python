# messaging_app/chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation  # <-- IMPORT THE CUSTOM PERMISSION

# This ViewSet handles all actions for Messages within a Conversation
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    
    # This is the crucial line that applies our rule.
    # The default 'IsAuthenticated' runs first, then this one.
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        This queryset is filtered to only return messages from the specific
        conversation requested in the URL.
        It's an additional security layer for the list view.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        return Message.objects.filter(conversation__pk=conversation_pk)

    def perform_create(self, serializer):
        """
        When a new message is created (sent), we automatically associate it
        with the conversation from the URL and the currently logged-in user.
        """
        conversation_pk = self.kwargs.get('conversation_pk')
        conversation = Conversation.objects.get(pk=conversation_pk)
        # The has_permission check has already verified the user is a participant.
        serializer.save(sender=self.request.user, conversation=conversation)