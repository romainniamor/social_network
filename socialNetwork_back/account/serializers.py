from .models import User, FriendRequest
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'name', 'email', 'friends_counter', 'posts_counter', 'get_avatar' ]

class FriendRequestSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = FriendRequest
        fields = ('id', 'created_by')