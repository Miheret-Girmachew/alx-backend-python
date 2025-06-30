from rest_framework import generics

from .models import Conversation 
from .serializers import ConversationSerializer 
from .auth import IsOwnerOrParticipant
class ConversationDetailView(generics.RetrieveAPIView):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    
    permission_classes = [IsOwnerOrParticipant]