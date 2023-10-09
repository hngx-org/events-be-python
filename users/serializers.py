from rest_framework import serializers
from .models import CustomUser,Group,User_Groups
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser


#@parser_classes([JSONParser])
class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    
    def create(self, validated_data):
        user = CustomUser(
          email=validated_data['email'],
          name=validated_data['name'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True  
        user.is_staff = True
        
        user.save()
        return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
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

