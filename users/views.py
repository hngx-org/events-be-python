import base64
import uuid
from django.shortcuts import render,redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from .serializers import AddFriendToGroupSerializer, Groupserializer, AppearanceSerializer, LanguageRegionSerializer
from .models import Group, User_Groups, Preferences
from authlib.integrations.django_client import OAuth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
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
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer

from django.core.files.base import ContentFile
from django.http import JsonResponse


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
    #permission_classes = (IsAuthenticated,)

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
            print("ues")

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


class ChangeProfileUser(generics.UpdateAPIView):
    """"""
    pass


class ContactUsView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        if user and user.email:
            success = send_mail(
                subject="Help and Support",
                message="Test Help and support",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False
            )
            if success:
                return Response({"message": "Mail successful"})
            else:
                return Response({"message": "Mail unsuccessful"})
        return Response({"message": "Not logged in"})


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
    #permission_classes = [IsAuthenticated]
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

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        user_id = self.request.user.id
        userSoc = get_object_or_404(UserSocialAuth, user_id=user_id)
        user = CustomUser.objects.get(email=userSoc.uid)
        if serializer.is_valid():
            group_name = serializer.validated_data.get('group_name')
            instance = serializer.save(admin=user,group_name=group_name)
            base64_img = serializer.validated_data.pop('base64_img')
            unique_id = str(uuid.uuid4())[:8]
            c_title = f'group_img_{unique_id}'
            img_data = base64.b64decode(base64_img)
            f = ContentFile(img_data)
            instance.image.save(f'{c_title}.jpg', f, save=True)
            instance.friends.add(user)
            friend_emails = serializer.validated_data.pop('friend_emails')
            print(friend_emails)
            for email in friend_emails:
                try:
                    friend = CustomUser.objects.get(email=email)
                    instance.friends.add(friend)
                    Ge = User_Groups.objects.create(group=instance, user=friend)
                except user.DoesNotExist:
                    return Response({"a user you are trying to add does not exist"},status=status.HTTP_404_NOT_FOUND)
        response ={
                "id": instance.pk,
                "group_name": instance.group_name,
                "admin": instance.admin.username,
                "image": instance.image.url,
                "friends": [ friend.pk for friend in instance.friends.all()],
                "created_at": instance.created_at,
                "updated_at": instance.updated_at
            }
        return JsonResponse(response, status=status.HTTP_201_CREATED)
    
    # def post(self, request, *args, **kwargs):
    #     serializer = Groupserializer(data=request.data)
    #     if serializer.is_valid():
    #         user_id = request.user.id
    #         user = get_object_or_404(UserSocialAuth, user_id=user_id)
    #         self.perform_create(serializer)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddFriendToGroup(generics.CreateAPIView):
    serializer_class = AddFriendToGroupSerializer
    def post(self, request, group_id):
        group = Group.objects.get(pk=group_id)
        serializer = AddFriendToGroupSerializer(data=request.data)
        user_id = request.user.id
        userSoc = get_object_or_404(UserSocialAuth, user_id=user_id)
        user = CustomUser.objects.get(email=userSoc.uid)

        if serializer.is_valid():
            if group.admin == user:
                friend_emails = serializer.validated_data.get('friend_emails')
                for email in friend_emails:
                    try:
                        friend = CustomUser.objects.get(uid=email)
                        group.friends.add(friend)
                        User_Groups.objects.create(group=group, user=friend)
                    except user.DoesNotExist:
                        return Response({"a user you are trying to add does not exist"},status=status.HTTP_404_NOT_FOUND)
                return Response({"message":"friend have been Added successfully"},status=status.HTTP_201_CREATED)
            return Response({"detail":"you are not the admin of this group"},status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RetrieveGroupApiView(generics.RetrieveAPIView):
    #permission_classes=[IsAuthenticated]
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
    #permission_classes=[IsAuthenticated]
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
    #permission_classes=[IsAuthenticated]
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
    #permission_classes = [IsAuthenticated]
    serializer_class = Groupserializer

    def get(self, request, *args, **kwargs):
        try:
            userSoc = get_object_or_404(UserSocialAuth, id=request.user.id)
            user = CustomUser.objects.get(email=userSoc.uid)
            created_groups = Group.objects.filter(admin=user)
            serializer = Groupserializer(created_groups, many=True)
            data = {'user groups': serializer.data}
            return Response(data, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'detail': 'No groups found for the user'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'An error occurred: {}'.format(str(e))}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetUserGroupDetail(APIView):
    #permission_classes=[IsAuthenticated]
    def get(self,request):
        user= get_object_or_404(CustomUser,email=request.user.email)
        groups = Group.objects.filter(Q(admin=user) | Q(friends=user))
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
    # permission_classes= []
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'

class GetUserDetailViews(APIView):
     # permission_classes= [AllowAny]
    permission_classes= [AllowAny]
    def get(self,request,email):
        print(email)
        print(CustomUser.objects.all())
        user=get_object_or_404(CustomUser,email=email)
        print(user)
        serializer=UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class AppearanceSetting(APIView):
    #permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=AppearanceSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_description="Save preferred appearance"
    )
    @action(detail=False, methods=['post'])
    def post(self, request):
        user_id = request.user.id
        userSoc = UserSocialAuth.objects.get(user_id=user_id)
        #userSoc = get_object_or_404(UserSocialAuth, user_id=user_id)
        print(userSoc)

        user = CustomUser.objects.get(email=userSoc.uid)

        
        serializer = AppearanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        appearance = serializer.validated_data['appearance']

        # Update or create the user's appearance setting
        preferences, created = Preferences.objects.get_or_create(user=user)
        preferences.appearance = appearance
        preferences.save()

        return Response({'message': 'Appearance setting updated successfully'}, status=status.HTTP_200_OK)



class LanguageRegionSettings(APIView):

    #permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=LanguageRegionSerializer,
        responses={200: 'Success', 400: 'Bad Request'},
        operation_description="Save preferred appearance"
    )
    @action(detail=False, methods=['post'])
    def post(self, request):
            user_id = request.user.id
            userSoc = get_object_or_404(UserSocialAuth, user_id=user_id)
            user = CustomUser.objects.get(email=userSoc.uid)

            serializer = LanguageRegionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            language = serializer.validated_data['language']
            region = serializer.validated_data['region']

            # Update or create the user's language and region settings
            preferences, created = Preferences.objects.get_or_create(user=user)
            preferences.language = language
            preferences.region = region
            preferences.save()

            return Response({'message': 'Language and region settings updated successfully'}, status=status.HTTP_200_OK)
        


class SingleNotificationView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_read = True  # Mark the notification as read
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class AllNotificationsView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


    def list(self, request, *args, **kwargs):
        # Calculate the count of unread notifications
        unread_count = Notification.objects.filter(is_read=False).count()
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "notifications": serializer.data,
            "unread_count": unread_count
        }
        return Response(data)
