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
        fields = ['pk','group_name','admin','created_at','updated_at']

