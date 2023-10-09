from django.shortcuts import render,redirect
from rest_framework import generics
from rest_framework.response import Response
from django.views import View
from .serializers import UserSerializer,Groupserializer, User_GroupsSerializer
from .models import CustomUser,Group, User_Groups
from authlib.integrations.django_client import OAuth
from django.contrib.auth import get_user_model
from rest_framework import status
from django.urls import reverse
import uuid
from .authentication import AuthenticationMiddleware, IsAuthenticatedUser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache
from itsdangerous import URLSafeTimedSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q
from rest_framework.decorators import api_view
from users.serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import login



class RegisterUser(generics.CreateAPIView):
    """
        Register new user and return the user the signup user up data, including sending an otp to email
        address of the user for verifiication
    """
    permission_classes = []
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    

    def create(self, request, *args, **kwargs):
        """OTP verification and validation"""
        
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_instance = serializer.save()
        
        # Get the serialized user data
        
        res = {"message": "Token sent!", "code": 200, "data": serializer.data}
        return Response(res, status=status.HTTP_200_OK)
class newLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = ()
    
    def post(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise AuthenticationFailed('Invalid data. Check your email and password.')

        try:
            email = serializer.initial_data['email']
            password = serializer.initial_data['password']
        except:
            raise AuthenticationFailed('Email and password required')

        try:
            
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                raise AuthenticationFailed('Invalid email or password.')

            
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid email or password.')

        
        try:
            if serializer.is_valid():
    
                tokens = serializer.validated_data
                custom_data = {
                    'access': str(tokens['access']),
                    'refresh': str(tokens['refresh']),
                    'user_id': user.id,
                }
                return Response(custom_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
        print("hek")
        
        
        return Response({"serializer.errors":"hi"}, status=status.HTTP_400_BAD_REQUEST)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile',
    }
)


# Create your views here.
class UserView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [IsAuthenticatedUser]
    
class SingleUserView(generics.RetrieveUpdateAPIView):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [IsAuthenticatedUser]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Set the lookup field to 'id'
    
    
class LoginView(View):
    def get(self, request):
        redirect_uri = request.build_absolute_uri(reverse('auth'))
        return oauth.google.authorize_redirect(request, redirect_uri)


class AuthView(APIView):
    def post(self,request):
        data = request.data
        name = data.get("name")
        email = data.get("email")
        picture = data.get("photoUrl")
        id = data.get("id")
        print(id)
        
        try:
            user = CustomUser.objects.get(id=id)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(email=email, id=str(id), name=name, avatar=picture)
            
        serializer = URLSafeTimedSerializer(AuthenticationMiddleware.secret_key)
        session_token = serializer.dumps(str(user.id))

        
            
        data = {
            "success": True,
            "user_id": id,
            "session_token": session_token,
            "status": 200
        }
        
        return Response(data)
        
        
    def get(self, request):
        token = oauth.google.authorize_access_token(request)
        email = token.get('userinfo', {}).get('email')
        name = token.get('userinfo', {}).get('name')
        picture = token.get('userinfo', {}).get('picture')
        access_token = token.get('access_token', {})
        id = token.get('userinfo', {}).get('sub')
        access_token = token.get('access_token', {})

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            user = CustomUser.objects.create(email=email, user_id=str(id), name=name, avatar=picture)
            
        # Set the is_active status in Redis
        cache_key = f'user_active_status:{user.id}'
        cache.set(cache_key, True)

        # Generate a session token
        serializer = URLSafeTimedSerializer(AuthenticationMiddleware.secret_key)
        session_token = serializer.dumps(str(user.id))
        
        data = {
            "success": True,
            "user_id": id,
            "session_token": session_token,
            "status": 200
        }
        
        response = Response(data, status=200)

        return response
    

class CreateGroupApiView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    
    def post(self, request, *args, **kwargs):
        serializer = Groupserializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save(admin=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    


class RetrieveGroupApiView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    lookup_field = 'pk'

class UpdateGroupApiView(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    lookup_field = 'pk'

    


@api_view(["GET"]) 
def GetUserGroupsApiView(request, *args, **kwargs):
    method = request.method

    if method == "GET":
        user = request.user
        if user.is_authenticated:
            # Filter groups based on the user who created them
            created_groups = Group.objects.filter(admin=user)
            serializer = Groupserializer(created_groups, many=True)
            return Response(serializer.data)
        
class editUserGroup(generics.UpdateAPIView):
    queryset = Group.objects.all()
    serializer = User_GroupsSerializer
        