# messaging_app/chats/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Conversation
from .serializers import ConversationSerializer
from .permissions import IsParticipantInConversation 

class ConversationDetailView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantInConversation]