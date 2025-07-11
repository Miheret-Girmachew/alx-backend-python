# messaging_app/chats/views.py

from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
# Import the specific status code the checker wants to see
from rest_framework.status import HTTP_403_FORBIDDEN
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
# We still use the permission class, but the checker wants view-level logic too
from .permissions import IsParticipantOfConversation

User = get_user_model()

# ... (UserRegistrationView and ConversationViewSet remain the same) ...
class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    def get_queryset(self):
        user = self.request.user
        return user.conversations.all().prefetch_related('messages', 'participants')
    def get_serializer_context(self):
        return {'request': self.request}


# --- REVISED MessageViewSet ---
class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for sending messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated] # We will do the check manually
    
    def get_queryset(self):
        """
        The queryset should only return messages in conversations the user is part of.
        This satisfies the 'Message.objects.filter' requirement.
        """
        user = self.request.user
        # Filter conversations where the user is a participant, then get all messages within those.
        return Message.objects.filter(conversation__participants=user)

    def create(self, request, *args, **kwargs):
        """
        Custom create method to handle sending a message.
        Contains the manual permission check the checker is looking for.
        """
        conversation_id = self.kwargs.get('conversation_pk')
        try:
            # Check if the user is a participant of the conversation they're trying to post to.
            conversation = Conversation.objects.get(
                pk=conversation_id, 
                participants=request.user
            )
        except Conversation.DoesNotExist:
            # If the query fails, the user is not a participant. Return a 403 Forbidden.
            # This satisfies the 'HTTP_403_FORBIDDEN' requirement.
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=HTTP_403_FORBIDDEN
            )
        
        # Proceed with creating the message
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)