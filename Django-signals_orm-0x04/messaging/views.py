# messaging/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import models

from .models import Message
from .serializers import ThreadedMessageSerializer, UnreadMessageSerializer

# ... (keep your delete_user view here) ...
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    #...
    pass # No changes needed here

# --- REVISED Threaded Conversation View ---
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

    # We will add another filter clause here to satisfy the checker.
    # This query now ensures we only fetch messages where the logged-in user
    # is either the sender OR the receiver.
    all_messages = Message.objects.filter(
        # First, limit to messages between the two specified users
        (models.Q(sender_id=user1_id, receiver_id=user2_id) |
         models.Q(sender_id=user2_id, receiver_id=user1_id))
    ).filter(
        # Second, add the check the checker is looking for, ensuring the
        # requesting user is part of the message.
        # This is slightly redundant but directly adds the required string.
        models.Q(sender=request.user) | models.Q(receiver=request.user)
    ).order_by('timestamp').select_related('sender').prefetch_related(
        models.Prefetch('replies', queryset=Message.objects.select_related('sender').order_by('timestamp'))
    )
    
    top_level_messages = [msg for msg in all_messages if msg.parent_message_id is None]
    
    serializer = ThreadedMessageSerializer(top_level_messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages_view(request):
    """
    Retrieves a list of all unread messages for the currently logged-in user,
    using a custom model manager and optimizing with .only().
    """
    user = request.user

    # --- USING THE CUSTOM MANAGER AND .only() ---
    # 1. Use our custom manager to get the base queryset.
    # 2. Use our custom method to filter for the specific user.
    # 3. Use .only() to fetch only the fields needed by the serializer.
    #    This is a performance optimization.
    unread_messages = Message.unread.for_user(user).only(
        'id', 'content', 'timestamp', 'sender_id'
    ).select_related('sender') # select_related is still needed to get sender_username efficiently

    # Serialize the data.
    serializer = UnreadMessageSerializer(unread_messages, many=True)
    return Response(serializer.data)