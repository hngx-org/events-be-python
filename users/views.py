from django.shortcuts import render,redirect
from rest_framework import generics
from rest_framework.response import Response
from django.views import View
from .serializers import Groupserializer
from .models import Group, User_Groups
from authlib.integrations.django_client import OAuth
from rest_framework import status
# from .authentication import IsAuthenticatedUser
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.cache import cache
from itsdangerous import URLSafeTimedSerializer
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from django.db.models import Q
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from social_django.models import UserSocialAuth
from .permissions import IsAuthenticatedSSO
from social_django.utils import load_strategy
from rest_framework_simplejwt.tokens import RefreshToken

class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)

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
                # 'access_token': social_auth.extra_data.get('access_token'),
            }

            # Generate a new access token using SimpleJWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            user_data['access_token'] = access_token
            user_data['refresh_token'] = refresh_token

            return Response(user_data, status=status.HTTP_200_OK)

        except UserSocialAuth.DoesNotExist:
            return Response({'error': 'User is not connected via SSO'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': f'Error occurred: {err}'}, status=status.HTTP_401_UNAUTHORIZED)

import requests
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        access_token = request.user.social_auth.get(provider='google-oauth2').extra_data['access_token']
        revoke_url = f'https://accounts.google.com/o/oauth2/revoke?token={access_token}'
        response = requests.get(revoke_url)
        
        if response.status_code == 200 or response.status_code == 400:
            # Successfully logged out from Google or token is already invalid
            request.session.clear()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        else:
            # Handle other potential errors
            error_message = response.text
            return Response({'error': f'Failed to log out. Response: {error_message}'}, status=status.HTTP_400_BAD_REQUEST)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile',
    }
)



class CreateGroupApiView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    
    def post(self, request, *args, **kwargs):
        serializer = Groupserializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            admin_instance = get_object_or_404(UserSocialAuth, user_id=user_id)
            serializer.save(admin=admin_instance)
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
        created_groups= Group.objects.filter(admin=get_object_or_404(UserSocialAuth,id=request.user.id))
        serializer = Groupserializer(created_groups, many=True)
        data = {'user groups': serializer.data}
        return Response(data, status=status.HTTP_200_OK)
