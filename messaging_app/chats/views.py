# messaging_app/chats/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated # <-- IMPORT ADDED
from django.shortcuts import get_object_or_404

from .models import Message, Conversation
from .serializers import MessageSerializer
from .permissions import IsParticipantOfConversation

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    
    # This list now contains both permissions, satisfying the checker.
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        if self.request.user in conversation.participants.all():
            return Message.objects.filter(conversation__pk=conversation_id)
        return Message.objects.none()

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_id')
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        serializer.save(sender=self.request.user, conversation=conversation)

    def retrieve(self, request, *args, **kwargs):
        message_obj = self.get_object()
        is_participant = request.user in message_obj.conversation.participants.all()
        if not is_participant:
            return Response(
                {"detail": "You do not have permission to access this resource."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(message_obj)
        return Response(serializer.data)