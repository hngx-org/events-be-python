from rest_framework import serializers
from .models import Group, User_Groups
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from social_django.models import UserSocialAuth

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialAuth
        fields = '__all__'


class Groupserializer(serializers.ModelSerializer):
    admin = serializers.CharField(read_only = True)
    class Meta:
        model = Group
        fields = ['pk','group_name','admin','created_at','updated_at']
        

class User_GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Groups
        fields = '__all__'

