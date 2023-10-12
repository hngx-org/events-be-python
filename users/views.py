from rest_framework import generics
from rest_framework.response import Response
from .serializers import Groupserializer
from .models import Group
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from social_django.models import UserSocialAuth
from events.serializers import userGroupsSerializerGet
from events.serializers import EventsSerializer
from django.urls import reverse
import requests
from.models import CustomUser

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

