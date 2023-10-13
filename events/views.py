from django.urls import reverse
from rest_framework import status, generics
from rest_framework.generics import UpdateAPIView

from users.models import User_Groups
from .models import Events, InterestinEvents
from django.contrib.auth.models import Group
from .serializers import EventsSerializer, Calenderserializer, InterestinEventsSerializer, userGroupsSerializer, GetEventsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q 
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from social_django.models import UserSocialAuth


class CreateEventView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    message = "You need to join the group to perform this action. Ask the group admin to add you."



    def post(self, request, *args, **kwargs):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            user_id = request.user.id
            user = get_object_or_404(UserSocialAuth, user_id=user_id)
            group_id = serializer.validated_data.get('group') 
            
            if group_id:
                try:
                    user_group = User_Groups.objects.get(group_id=group_id, user=user)
                    serializer.save(creator=user)
                    return Response(serializer.data, status=status.HTTP_200_OK )
                except User_Groups.DoesNotExist:
                    return Response(
                        {"detail": self.message},
                        status=status.HTTP_302_FOUND,
                    )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        """
        Provides a get method handler that returns all events.
        """
        print(request.user)
        queryset = Events.objects.all()
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data)


class getEvent(APIView):
    """Handles getting event by id"""
    permission_classes=[IsAuthenticated]
    def get(self, request, event_id):

        try:
            event = Events.objects.get(id=event_id)
            serilizer = GetEventsSerializer(event, context={'request': request})
            return Response(serilizer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "event does not exist"}, status=status.
            HTTP_404_NOT_FOUND)


class getGroupEvents(APIView):
    """Handles getting events in a group"""
    permission_classes=[IsAuthenticated]
    def get(self, request, group_id):

        try:
            get_object_or_404(Group, pk=group_id)
            event = Events.objects.filter(group=group_id)
            serilizer = GetEventsSerializer(event, context={'request': request}, many=True)
            if not event.exists():
                return Response({"error": "No event for this group"}, status=status.
            HTTP_404_NOT_FOUND)
            return Response(serilizer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.
            HTTP_404_NOT_FOUND)


class UpdateEventView(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    lookup_url_kwarg = 'event_uuid'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchEventView(APIView):
    """
    Search events by keywords and return events.
    """
    permission_classes=[IsAuthenticated]
    def get(self, request, keyword):
        try:
            events = Events.objects.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
            if not events.exists():
                return Response({"Message":"No event containing '{}' found!".format(keyword)}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response({"error": "no result"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class UpdateEventView(UpdateAPIView):
    permission_classes=[IsAuthenticated]
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    lookup_url_kwarg = 'event_uuid'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CalenderView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    queryset= Events.objects.all()
    serializer_class = Calenderserializer
    def retrieve(self, request, *args, **kwargs):
        Interests= InterestinEvents.objects.filter(user=get_object_or_404(UserSocialAuth,id=request.user.id))
        data=[]
        for interest in Interests:
            event=interest.event
            serializer = Calenderserializer(event)
            data.append(serializer.data)
        context = {'calenderDetail': data}
        return Response(context, status=status.HTTP_200_OK)

class EventDelView(generics.DestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset= Events.objects.all()
    serializer_class=EventsSerializer
    lookup_field='id'
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Event deleted successfully."}, status=status.HTTP_200_OK)

class JoinEvent(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)
        user_id = request.user.id
        
        user = get_object_or_404(UserSocialAuth, user_id=user_id)
         
        serializer = InterestinEventsSerializer(data=request.data, context={'event': event, 'user': user})

        if serializer.is_valid():
            
            InterestinEvents.objects.get_or_create(event=event, user=user)
            return Response({f"message": "Success! You have expressed interest in the {event.title} event."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class LeaveEvent(APIView):
    permission_classes=[IsAuthenticated]
    def delete(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)
        user_id = request.user.id
        user = get_object_or_404(UserSocialAuth, user_id=user_id)
        try:
            interest = InterestinEvents.objects.get(event=event, user=user)
            interest.delete()
            return Response({"message": "You have successfully deleted your interest in this event."}, status=status.HTTP_204_NO_CONTENT)
        except InterestinEvents.DoesNotExist:
            return Response({"message": "You have not expressed interest in this event."}, status=status.HTTP_404_NOT_FOUND)

class OtherUserGroupEvents(generics.ListAPIView):
    serializer_class = EventsSerializer

    def get_queryset(self):
        # Get the current user
        user_id = self.request.user.id
        user = get_object_or_404(UserSocialAuth, user_id=user_id)

        # Get the groups that the current user is a member of
        user_groups = user.Groupfriends.all()

        # Get friends of the current user who are in the same groups
        friends_in_same_groups = UserSocialAuth.objects.filter(
            Groupfriends__in=user_groups
        )

        # Get events created by those friends
        events_created_by_friends = Events.objects.filter(
            creator__in=friends_in_same_groups
        )

        return events_created_by_friends


                       