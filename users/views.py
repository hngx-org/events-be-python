from rest_framework import generics
from rest_framework.response import Response
from .serializers import Groupserializer
from .models import Group
from authlib.integrations.django_client import OAuth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from social_django.models import UserSocialAuth
from users.serializers import UserSerializer
from events.serializers import EventsSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from comments.models import Comment
from events.models import Events
from comments.serializers import CommentpicSerializer
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
    permission_classes=[IsAuthenticated]

    queryset = Group.objects.all()
    serializer_class = Groupserializer
    def get(self, request, *args, **kwargs):
        created_groups= Group.objects.filter(admin=get_object_or_404(UserSocialAuth,id=request.user.id))
        serializer = Groupserializer(created_groups, many=True)
        data = {'user groups': serializer.data}
        return Response(data, status=status.HTTP_200_OK)

class GetUserGroupDetail(APIView):
    def get(self,request):
        user= get_object_or_404(UserSocialAuth,id=request.user.id)
        groups = Group.objects.filter(admin=user)
        group_info=[{
            'groupCount':len(groups)
        }]
        for group in groups:
            events=Events.objects.filter(group=group)
            eventandcomment=[]
            for event in events:
                events_serialize=EventsSerializer(event)
                comments=Comment.objects.filter(event_id=get_object_or_404(Events,id=event.id))
                comments_serialize=CommentpicSerializer(comments,many=True)
                event_data=events_serialize.data
                event_data['comment']=len(comments)
                event_data['commentpics']=comments_serialize.data
                eventandcomment.append(event_data)
            group_info.append({
                'group_name': group.group_name,
                'eventCount': len(events),
                'events':eventandcomment,
            })
        return Response(group_info,status=status.HTTP_200_OK)
# class GetUserDetailView(generics.RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'email'

 