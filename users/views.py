from django.shortcuts import render,redirect
from rest_framework import generics
from rest_framework.response import Response
from django.views import View
from .serializers import UserSerializer,Groupserializer
from .models import CustomUser,Group, User_Groups
from authlib.integrations.django_client import OAuth
from rest_framework import status
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
from django.shortcuts import get_object_or_404
from social_django.models import UserSocialAuth
from .permissions import IsAuthenticatedSSO

from django.contrib.auth import login
from social_django.utils import psa
from rest_framework_simplejwt.tokens import RefreshToken

class UserProfileView(APIView):
    permission_classes = (IsAuthenticatedSSO,)

    def get(self, request):
        user = request.user

        try:
            # Try to get the user's social auth information
            social_auth = UserSocialAuth.objects.get(user=user)

            # Extract user data from the social auth instance
            user_data = {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'provider': social_auth.provider,
                'social_id': social_auth.uid,
                'access_token': social_auth.extra_data.get('access_token'),
            }

            # Generate a new access token using SimpleJWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            user_data['new_access_token'] = access_token
            user_data['new_refresh_token'] = refresh_token

            return Response(user_data, status=status.HTTP_200_OK)

        except UserSocialAuth.DoesNotExist:
            return Response({'error': 'User is not connected via SSO'}, status=status.HTTP_BAD_REQUEST)
        except Exception as err:
            return Response({'error': f'Error occurred: {err}'}, status=status.HTTP_INTERNAL_SERVER_ERROR)


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
    # authentication_classes = [AuthenticationMiddleware]
    permission_classes = [IsAuthenticated]
    
class SingleUserView(generics.RetrieveUpdateAPIView):
    authentication_classes = [AuthenticationMiddleware]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'  # Set the lookup field to 'id'
    

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

    def perform_update(self, serializer):
        user = self.request.user
        group = self.get_object()  
        if group.admin == user:
            serializer.save()
            return Response({"message": "group updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "user can't be found."}, status=status.HTTP_401_UNAUTHORIZED)
    
class DeleteGroupApiView(generics.DestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        user = self.request.user
        group = self.get_object()  
        if group.admin == user:
            super().perform_destroy(instance)
            return Response({"message": "group deleted successfully."}, status=status.HTTP_2 )
        else:
            return Response({"error": "user is not an admin."}, status=status.HTTP_401_UNAUTHORIZED)
    
class GetUserGroupsApiView(generics.ListAPIView):
    # permission_classes=[IsAuthenticated]

    queryset = Group.objects.all()
    serializer_class = Groupserializer
    def get(self, request, *args, **kwargs):
        created_groups= Group.objects.filter(admin=get_object_or_404(CustomUser,id=request.user.id))
        serializer = Groupserializer(created_groups, many=True)
        data = {'user groups': serializer.data}
        return Response(data, status=status.HTTP_200_OK)

# @api_view(["GET"]) 
# def GetUserGroupsApiView(request, *args, **kwargs):
#     method = request.method

#     if method == "GET":
#         user = request.user
#         User = get_object_or_404(CustomUser,id=user.id)
#         created_groups = Group.objects.filter(admin=User)
#         serializer = Groupserializer(created_groups, many=True)
#         return Response(serializer.data)   
#     return Response({"error":"user does not exist"},status=status.HTTP_401_UNAUTHORIZED)
        
# class editUserGroup(generics.UpdateAPIView):
#     queryset = Group.objects.all()
#     serializer = User_GroupsSerializer
        
from social_django.models import UserSocialAuth
user = UserSocialAuth.objects.all()
