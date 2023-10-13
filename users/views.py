from django.shortcuts import render,redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from .serializers import AddFriendToGroupSerializer, Groupserializer
from .models import Group, User_Groups
from authlib.integrations.django_client import OAuth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from social_django.models import UserSocialAuth
from users.serializers import UserSerializer
from events.serializers import EventsSerializer
from django.urls import reverse
import requests
from comments.models import Comment
from events.models import Events
from comments.serializers import CommentpicSerializer
from  .models import CustomUser
class UserProfileView(APIView):
    """
    Redirect user after signing in using SSO and return the following properties of the user as it is on social auth
        username: on gmail
        email: on gmail
        names: first_name and last_name
        social_auth_provider: e.g google
        social_id: uidd associated with the user on the social_auth
        picture: profile picture of the user
        
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        try:
            social_auth = UserSocialAuth.objects.get(user=user)

            # Extract user data from the social auth instance
            user_data = {
                'message': 'User login successful',
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'provider': social_auth.provider,
                'social_id': social_auth.uid,
            }

            # Fetch the user's profile picture using the get_profile_pcture function
            access_token = social_auth.extra_data.get('access_token')
            picture_url = self.get_profile_picture(access_token)

            user_data['profile_image'] = picture_url


            # Check if the user already exists by email or username
            existing_user = CustomUser.objects.filter(email=user.email) | CustomUser.objects.filter(username=user.username)
            if existing_user.exists():
                pass
            else:
                new_user = CustomUser(username=user.username, email=user.email, profile_picture=picture_url)
                new_user.save()

            return Response(user_data, status=status.HTTP_200_OK)


        except UserSocialAuth.DoesNotExist:
            return Response({'error': 'User is not connected via SSO'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as err:
            return Response({'error': f'Error occurred: {err}'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_profile_picture(self, access_token):
        """Acess the user profile picture using the access token generated from the SO"""
        try:
            url = 'https://www.googleapis.com/oauth2/v2/userinfo'
            params = {'access_token': access_token}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                user_data = response.json()
                profile_picture = user_data.get('picture')
                return profile_picture
            else:
                return None  

        except Exception as e:
            return None


class GoogleLoginView(APIView):
    """
    Return an endpoint that will redirect user to permission page
    to generate a session token that will log them in
    """

    def post(self, request):
        auth_url = reverse('social:begin', args=['google-oauth2'])
        return Response({'auth_url': request.build_absolute_uri(auth_url)}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """ 
        Get and revoke the session token to log user out.
    """
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


class CreateGroupApiView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = Groupserializer

    def perform_create(self, serializer):
        user_id = self.request.user.id
        user = get_object_or_404(UserSocialAuth, user_id=user_id)
        instance = serializer.save(admin=user)
        instance.friends.add(user)
        friend_emails = serializer.validated_data.pop('friend_emails')
        for email in friend_emails:
            try:
                friend = UserSocialAuth.objects.get(uid=email)
                instance.friends.add(friend)
                User_Groups.objects.create(group=instance, user=friend)
            except user.DoesNotExist:
                return Response({"a user you are trying to add does not exist"},status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = Groupserializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            user = get_object_or_404(UserSocialAuth, user_id=user_id)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddFriendToGroup(generics.CreateAPIView):
    serializer_class = AddFriendToGroupSerializer
    def post(self, request, group_id):
        group = Group.objects.get(pk=group_id)
        serializer = AddFriendToGroupSerializer(data=request.data)
        user_id = request.user.id
        user = get_object_or_404(UserSocialAuth, user_id=user_id)

        if serializer.is_valid():
            if group.admin == user:
                friend_emails = serializer.validated_data.get('friend_emails')
                for email in friend_emails:
                    try:
                        friend = UserSocialAuth.objects.get(uid=email)
                        group.friends.add(friend)
                        User_Groups.objects.create(group=group, user=friend)
                    except user.DoesNotExist:
                        return Response({"a user you are trying to add does not exist"},status=status.HTTP_404_NOT_FOUND)
                return Response({"message":"friend have been Added successfully"},status=status.HTTP_201_CREATED)
            return Response({"detail":"you are not the admin of this group"},status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class RetrieveGroupApiView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = Groupserializer
    lookup_field = 'pk'

    def get(self, request, pk, *args, **kwargs):
        try:
            group = get_object_or_404(Group, pk=pk)
            serializer = Groupserializer(group)
            events = group.events_set.all()
            events_serialize = EventsSerializer(events, many=True)
            data = {
                'group': serializer.data,
                'events': events_serialize.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "no result"}, status=status.HTTP_404_NOT_FOUND)
        





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
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'No groups found for the user'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'An error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserGroupDetail(APIView):
    permission_classes=[IsAuthenticated]
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
class GetUserDetailView(generics.RetrieveAPIView):
    permission_classes= [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

 