# messaging_app/chats/views.py

from rest_framework import viewsets, status  # <-- Ensure 'status' is imported
from rest_framework.response import Response  # <-- Ensure 'Response' is imported
from django.shortcuts import get_object_or_404

from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation # <-- The permission class is still vital

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        """
        Filters messages to the conversation specified in the URL.
        This is for the LIST view (e.g., /api/conversations/1/messages/).
        """
        conversation_id = self.kwargs.get('conversation_id')
        
       
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        if self.request.user in conversation.participants.all():
            return Message.objects.filter(conversation__pk=conversation_id)
        return Message.objects.none() # Return empty queryset if not a participant

    def perform_create(self, serializer):
        """
        Assigns the sender and conversation when creating a new message.
        """
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, pk=conversation_id)
      
        serializer.save(sender=self.request.user, conversation=conversation)

    def retrieve(self, request, *args, **kwargs):
        """
        Handles retrieving a SINGLE message (e.g., /api/conversations/1/messages/5/).
        We override it to add an explicit permission check.
        """
        message_obj = self.get_object()
        
        is_participant = request.user in message_obj.conversation.participants.all()

        if not is_participant:
           
            return Response(
                {"detail": "You do not have permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(message_obj)
        return Response(serializer.data)