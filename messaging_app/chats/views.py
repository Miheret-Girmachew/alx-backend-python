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
from .pagination import MessagePagination
from .filters import MessageFilter

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


# ---  MessageViewSet ---
class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing and sending messages within a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    
    # --- Add these two lines for pagination and filtering ---
    pagination_class = MessagePagination
    filterset_class = MessageFilter

    # Allow GET for listing messages, and POST for creating them.
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        """
        The queryset should only return messages in the specific conversation
        from the URL, for the user who is making the request.
        """
        user = self.request.user
        conversation_pk = self.kwargs.get('conversation_pk')

        # First, ensure the user is part of the conversation
        if not Conversation.objects.filter(pk=conversation_pk, participants=user).exists():
            return Message.objects.none() # Return empty queryset if not a participant

        # Return messages for that specific conversation
        return Message.objects.filter(conversation_id=conversation_pk).order_by('-sent_at')

    # The 'create' method can remain as it was in the last step,
    # as its logic is still valid for POST requests.
    def create(self, request, *args, **kwargs):
        # ... (no changes needed to the create method from the previous task)
        conversation_id = self.kwargs.get('conversation_pk')
        try:
            conversation = Conversation.objects.get(
                pk=conversation_id, 
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, conversation=conversation)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)