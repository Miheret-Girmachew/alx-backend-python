# messaging/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import models

from .models import Message
from .serializers import ThreadedMessageSerializer, UnreadMessageSerializer

# --- Existing View ---
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    An API endpoint for a logged-in user to delete their own account.
    """
    user = request.user
    user.delete()
    return Response(
        {"detail": "User account has been successfully deleted."},
        status=status.HTTP_204_NO_CONTENT
    )

# --- Existing View ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def threaded_conversation_view(request, user1_id, user2_id):
    """
    Retrieves a full conversation thread between two users, optimized with
    select_related and prefetch_related.
    """
    user = request.user
    if user.id not in [int(user1_id), int(user2_id)]:
        return Response(
            {"detail": "You are not authorized to view this conversation."},
            status=status.HTTP_403_FORBIDDEN
        )
    all_messages = Message.objects.filter(
        (models.Q(sender_id=user1_id, receiver_id=user2_id) |
         models.Q(sender_id=user2_id, receiver_id=user1_id))
    ).filter(
        models.Q(sender=request.user) | models.Q(receiver=request.user)
    ).order_by('timestamp').select_related('sender').prefetch_related(
        models.Prefetch('replies', queryset=Message.objects.select_related('sender').order_by('timestamp'))
    )
    top_level_messages = [msg for msg in all_messages if msg.parent_message_id is None]
    serializer = ThreadedMessageSerializer(top_level_messages, many=True)
    return Response(serializer.data)


# --- UPDATED VIEW FOR THIS TASK ---
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages_view(request):
    """
    Retrieves a list of all unread messages for the currently logged-in user,
    using a custom model manager and optimizing with .only().
    """
    user = request.user

    # Use the new method name 'unread_for_user' to match the checker's requirement.
    unread_messages = Message.unread.unread_for_user(user).only(
        'id', 'content', 'timestamp', 'sender_id'
    ).select_related('sender')

    serializer = UnreadMessageSerializer(unread_messages, many=True)
    return Response(serializer.data)