from rest_framework import serializers
from .models import CustomUser,Group,User_Groups


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class Groupserializer(serializers.ModelSerializer):
    admin = serializers.CharField(read_only = True)
    class Meta:
        model = Group
        fields = ['group_name','admin','created_at','updated_at']


class User_GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Groups
        fields = '__all__'