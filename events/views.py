from rest_framework import status, generics 
from rest_framework.generics import UpdateAPIView
from .models import Events, InterestInEvents
from django.contrib.auth.models import Group
from .serializers import userGroupsSerializer
from .serializers import EventsSerializer, Calenderserializer, InterestInEventsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
#from rest_framework.permissions import IsAuthenticated
from django.db.models import Q 
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated, AllowAny

class CreateEventView(generics.CreateAPIView):
    permission_classes = []
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    def post(self, request, *args, **kwargs):
        serializer = EventsSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class EventsView(APIView):
    permission_classes = []
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
    def get(self, request, event_id):

        try:
            event = Events.objects.get(id=event_id)
            serilizer = EventsSerializer(event, context={'request': request})
            return Response(serilizer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "event does not exist"}, status=status.
            HTTP_404_NOT_FOUND)
            

class UpdateEventView(UpdateAPIView):
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
    def get(self, request, keyword):
        try:
            events = Events.objects.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
        except:
            return Response({"error": "no result"}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventsSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    


class UpdateEventView(UpdateAPIView):
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
    # permission_classes=[IsAuthenticated]

    queryset= Events.objects.all()
    serializer_class = Calenderserializer
    def retrieve(self, request, *args, **kwargs):
        events= Events.objects.filter(creator=get_object_or_404(CustomUser,id=request.user.id))
        serializer = Calenderserializer(events, many=True)
        context = {'calenderDetail': serializer.data}
        return Response(context, status=status.HTTP_200_OK)

class EventDelView(generics.DestroyAPIView):
    # permission_classes=[IsAuthenticated]
    queryset= Events.objects.all()
    serializer_class=EventsSerializer
    lookup_field='id'
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Event deleted successfully."}, status=status.HTTP_200_OK)
    


class JoinEvent(APIView):
    def post(self, request, event_id):
        event = get_object_or_404(Events, id=event_id)

        serializer = InterestInEventsSerializer(data=request.data)

        if serializer.is_valid():
            if request.user.is_authenticated:
                InterestInEvents.objects.get_or_create(event=event, user=request.user)
                return Response({"message": "Success! You have expressed interest in the event."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message: Authentication required to express interest in the event, PLEASE REGISTER!. "}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)