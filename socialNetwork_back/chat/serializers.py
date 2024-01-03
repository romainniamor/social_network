from .models import Conversation, ConversationMessage
from account.serializers import UserSerializer
from rest_framework import serializers

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only = True, many=True)
    
    class Meta:
        model= Conversation
        fields= ['id', 'users', 'modified_at_formated', ]


class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model= ConversationMessage
        fields= ['id', 'created_by', 'created_at_formated', 'sent_to', 'body']


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        model= Conversation
        fields=['id', 'users', 'modified_at_formated', 'messages']


