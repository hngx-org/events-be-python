from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from social_django.models import UserSocialAuth
from users.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth
        fields = '__all__'


class Groupserializer(serializers.ModelSerializer):
    admin = serializers.CharField(read_only = True)
    class Meta:
        model = Group
        fields = ['pk','group_name','admin','image','friends','created_at','updated_at']
        

class User_GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroups
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'
class AddFriendToGroupSerializer(serializers.Serializer):
    friend_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=UserSocialAuth.objects.all())
    )