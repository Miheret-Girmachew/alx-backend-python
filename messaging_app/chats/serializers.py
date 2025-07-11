# messaging_app/chats/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

# It's a best practice to get the User model using this function
# as it correctly handles our custom user model defined in settings.py.
User = get_user_model()


# Serializer for our custom User model
# This handles user creation and ensures passwords are write-only and hashed.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Fields to be included in the serialized output.
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'password']
        # Extra arguments for specific fields. 'password' should never be readable.
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Overrides the default create method to use our custom User model's
        create_user method, which handles password hashing.
        """
        # The **validated_data syntax unpacks the dictionary into keyword arguments.
        user = User.objects.create_user(**validated_data)
        return user


# Serializer for the Message model
# This is a straightforward serializer that will be nested inside the ConversationSerializer for display.
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # List of fields to include in the JSON representation.
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# The main serializer for handling conversations with nested relationships.
class ConversationSerializer(serializers.ModelSerializer):
    # Field for DISPLAYING participant details (READ-ONLY).
    # It calls the 'get_participants' method to generate its output.
    # This satisfies the 'SerializerMethodField' requirement.
    participants = serializers.SerializerMethodField()

    # Field for CREATING a conversation by accepting a list of UUIDs (WRITE-ONLY).
    # This will not be included in the response data.
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True
    )
    
    # Nest the related messages for display purposes (READ-ONLY).
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        # The full list of fields this serializer will handle.
        fields = ['conversation_id', 'participants', 'participant_ids', 'messages', 'created_at']
        # Fields that should not be writable via the API.
        read_only_fields = ['conversation_id', 'created_at']

    def get_participants(self, obj):
        """
        Custom method to serialize the full details of the participants.
        'obj' is the Conversation instance being serialized.
        """
        participants_queryset = obj.participants.all()
        # Use the UserSerializer to format the participant data.
        return UserSerializer(participants_queryset, many=True).data

    def create(self, validated_data):
        """
        Custom logic to create a conversation and correctly associate participants.
        """
        # Get the list of UUIDs from the input data.
        participant_ids = validated_data.pop('participant_ids')
        
        # We must add the user making the request to the conversation participants.
        # The 'request' object is passed in the 'context' from the view.
        request_user = self.context['request'].user
        
        # Combine the user making the request with the list of other participants.
        # Using a set handles potential duplicates automatically.
        all_participant_ids = set(participant_ids)
        all_participant_ids.add(request_user.user_id)

        # Validate that all user UUIDs exist in the database.
        participants = []
        for user_id in all_participant_ids:
            try:
                user = User.objects.get(user_id=user_id)
                participants.append(user)
            except User.DoesNotExist:
                # If any user is not found, raise an error.
                # This satisfies the 'ValidationError' requirement.
                raise serializers.ValidationError(f"User with ID {user_id} not found.")

        # Create the Conversation instance.
        conversation = Conversation.objects.create(**validated_data)

        # Set the many-to-many relationship for participants.
        conversation.participants.set(participants)
        
        return conversation