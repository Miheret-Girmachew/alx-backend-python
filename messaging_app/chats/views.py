
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer

User = get_user_model()


# 1. A View for User Registration (A crucial, non-ViewSet part)
# We use generics.CreateAPIView for a simple POST-only endpoint.
class UserRegistrationView(generics.CreateAPIView):
    """
    An endpoint for creating new users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # We allow any user (authenticated or not) to access this endpoint.
    permission_classes = [permissions.AllowAny]


# 2. The ViewSet for Conversations
# A ModelViewSet provides full CRUD (Create, Retrieve, Update, Delete) functionality.
class ConversationViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and creating conversations.
    Provides `list`, `create`, `retrieve`, `update`, `partial_update`, and `destroy` actions.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipant] 
    def get_queryset(self):
        """
        This is a critical security and privacy step.
        This view should only return conversations that the currently
        authenticated user is a part of. It filters the default queryset.
        """
        user = self.request.user
        # The 'related_name' on the Conversation model's 'participants' field
        # was 'conversations', so we can access them via user.conversations.
        return user.conversations.all().prefetch_related('messages', 'participants')

    def get_serializer_context(self):
        """
        This is how we pass the 'request' object from the view to the serializer.
        Our ConversationSerializer needs it to automatically add the current user
        to the list of participants when creating a new conversation.
        """
        return {'request': self.request}


# 3. The ViewSet for Messages
# We only need 'create' functionality, so a simpler ViewSet is better.
class MessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for sending messages. We only implement the 'create' action.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This method is required by ModelViewSet, but we will primarily be creating
        messages, not listing all of them through this endpoint.
        Listing is handled by the nested serializer in ConversationViewSet.
        We'll filter to only messages sent by the user for completeness.
        """
        return Message.objects.filter(sender=self.request.user)
    
    def perform_create(self, serializer):
        """
        Custom logic that runs when a new message is created (POST request).
        The conversation ID is now retrieved from the URL kwargs.
        """
        # The nested router provides the parent's PK in the URL kwargs.
        conversation_id = self.kwargs.get('conversation_pk')
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        # Check if the user is a participant of the conversation.
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant of this conversation.")

        # Save the message with the sender and the conversation from the URL.
        serializer.save(sender=self.request.user, conversation=conversation)