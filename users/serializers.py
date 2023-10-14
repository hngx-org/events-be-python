from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Group, User_Groups
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from social_django.models import UserSocialAuth
from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth
        fields = '__all__'


class Groupserializer(serializers.ModelSerializer):
    admin = serializers.CharField(read_only = True)
    friend_emails = serializers.ListField(child=serializers.EmailField(), write_only=True,required=False)
    friends = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Group
        fields = ('id', 'group_name', 'admin', 'image', 'friends', 'created_at', 'updated_at', 'friend_emails')

    
    def create(self, validated_data):

       friend_emails = validated_data.pop('friend_emails')

       group = Group.objects.create(**validated_data)

       return group
        

class User_GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Groups
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields = '__all__'
class AddFriendToGroupSerializer(serializers.Serializer):
    friend_emails = serializers.ListField(child=serializers.EmailField(), write_only=True,)