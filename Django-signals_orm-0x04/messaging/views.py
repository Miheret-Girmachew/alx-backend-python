# messaging/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import models

# Import your models and the new serializer
from .models import Message
from .serializers import ThreadedMessageSerializer


# --- Existing View ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    An API endpoint for a logged-in user to delete their own account.
    This action is irreversible and will trigger cleanup signals.
    """
    user = request.user
    user.delete()
    return Response(
        {"detail": "User account has been successfully deleted."},
        status=status.HTTP_204_NO_CONTENT
    )


# --- New View for Threaded Conversations ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threaded_conversation_view(request, user1_id, user2_id):
    """
    Retrieves a full conversation thread between two users, optimized with
    select_related and prefetch_related to prevent N+1 query problems.
    """
    user = request.user
    
    # Security check: Ensure the requesting user is one of the participants.
    if user.id not in [int(user1_id), int(user2_id)]:
        return Response(
            {"detail": "You are not authorized to view this conversation."},
            status=status.HTTP_403_FORBIDDEN
        )

    # 1. Fetch all messages between the two users in a single, efficient query.
    #    - select_related('sender'): Joins the User table to get sender info in the same query.
    #    - prefetch_related('replies'): Fetches all replies for these messages in a separate, efficient query.
    #      We add another select_related('sender') inside the Prefetch for the replies themselves.
    all_messages = Message.objects.filter(
        (models.Q(sender_id=user1_id, receiver_id=user2_id) |
         models.Q(sender_id=user2_id, receiver_id=user1_id))
    ).order_by('timestamp').select_related('sender').prefetch_related(
        models.Prefetch('replies', queryset=Message.objects.select_related('sender').order_by('timestamp'))
    )

    # 2. Filter for top-level messages (those that are not replies).
    top_level_messages = [msg for msg in all_messages if msg.parent_message_id is None]
    
    # The prefetch_related has already attached the replies to each message object,
    # so no further database queries are needed. We can now serialize the data.
    
    # 3. Serialize the top-level messages. The recursive serializer will handle nesting the replies.
    serializer = ThreadedMessageSerializer(top_level_messages, many=True)
    return Response(serializer.data)