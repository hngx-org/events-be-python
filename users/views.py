from django.shortcuts import render,redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from django.views import View
from .serializers import Groupserializer, User_GroupsSerializer
from .models import Group, User_Groups
from authlib.integrations.django_client import OAuth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from social_django.models import UserSocialAuth
from events.serializers import userGroupsSerializerGet
from events.serializers import EventsSerializer
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
                'message':'User login successful',
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'provider': social_auth.provider,
                'social_id': social_auth.uid,
                #'profile_image':response['photos'][0]['url']
                # 'access_token': social_auth.extra_data.get('access_token'),
            }

            # Generate a new access token using SimpleJWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)


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
            instance=serializer.save(admin=admin_instance)
            friends = serializer.validated_data.get('friends')
            for friend in friends:
                print(friend, instance.pk)
                User_Groups.objects.create(group=instance, user=friend)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    

class RetrieveGroupApiView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    lookup_field = 'pk'

class UpdateGroupApiView(generics.UpdateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        user_id = self.request.user.id
        user = get_object_or_404(UserSocialAuth, user_id=user_id)
        group = self.get_object()  
        if group.admin == user:
            serializer.save()
            return Response({"message": "group updated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "user can't be found."}, status=status.HTTP_401_UNAUTHORIZED)
    
class DeleteGroupApiView(generics.DestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        user_id = self.request.user.id
        user = get_object_or_404(UserSocialAuth, user_id=user_id)
        group = self.get_object()  
        if group.admin == user:
            super().perform_destroy(instance)
            return Response({"message": "group deleted successfully."}, status=status.HTTP_204_NO_CONTENT )
        else:
            return Response({"error": "user is not an admin."}, status=status.HTTP_401_UNAUTHORIZED)

class JoinGroupView(generics.CreateAPIView):
    serializer_class = User_GroupsSerializer

    def create(self, request, *args, **kwargs):
        group_id = request.data.get('group')
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'message': 'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        user_id = request.user.id
        user = get_object_or_404(UserSocialAuth, user_id=user_id)
        if User_Groups.objects.filter(members=user, group=group).exists():
            return Response({'message': 'User is already in the group'}, status=status.HTTP_400_BAD_REQUEST)
        user_group = User_Groups(group=group)
        user_group.save()
        user_group.members.add(user)
        group.friends.add(user)


        return Response({'message': 'User joined the group'}, status=status.HTTP_201_CREATED) 
      
class GetUserGroupsApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = Groupserializer

    def get(self, request, *args, **kwargs):
        try:
            user_social_auth = get_object_or_404(UserSocialAuth, id=request.user.id)
            created_groups = Group.objects.filter(admin=user_social_auth)
            serializer = Groupserializer(created_groups, many=True)
            data = {'user groups': serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        except UserSocialAuth.DoesNotExist:
            return Response({'detail': 'UserSocialAuth not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'No groups found for the user'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'An error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserGroupDetail(APIView):
    def get(self,request):
        user= get_object_or_404(UserSocialAuth,id=request.user.id)
        groups = Group.objects.filter(admin=user)
        user_groupSerialize=userGroupsSerializerGet(groups,many=True)
        group_info=[{
            'groupCount':len(groups)
        }]
        for group in groups:
            events=group.events_set.all()
            events_serialize=EventsSerializer(events,many=True)
            group_info.append({
                'group_name': group.group_name,
                'eventCount': len(events),
                'events': events_serialize.data
            })
        return Response(group_info,status=status.HTTP_200_OK)
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
