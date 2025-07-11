
from rest_framework import serializers
from .models import User, Conversation, Message

# Serializer for the Message model
# This is a simple ModelSerializer. It will be nested inside the ConversationSerializer.
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # We list the fields we want to include in the JSON output.
        fields = ['message_id', 'sender', 'message_body', 'sent_at']


# Serializer for our custom User model
# This serializer will handle creating users and making sure passwords are handled securely.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # List all the fields that should be used for serialization.
        # 'password' is write-only, we don't want to ever send it back in a response.
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # We override the create method to handle password hashing.
    def create(self, validated_data):
        # The .create_user() method on our custom User model will handle hashing the password.
        user = User.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


# Serializer for the Conversation model
# This is where we handle the nested relationships.
class ConversationSerializer(serializers.ModelSerializer):
    # This line is the key to nesting.
    # It tells DRF to use the MessageSerializer for the 'messages' field.
    # 'many=True' is because a conversation can have many messages.
    # 'read_only=True' means we can't create messages by writing to this field,
    # which is good practice. We'll have a separate endpoint for that.
    messages = MessageSerializer(many=True, read_only=True)
    
    # We also want to see the details of the participants, not just their IDs.
    # We use the UserSerializer, but we only want to read the data (read_only).
    # We can't add participants to a conversation through this serializer.
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        # Include the nested 'messages' and 'participants' fields in the final JSON.
        fields = ['conversation_id', 'participants', 'messages', 'created_at']