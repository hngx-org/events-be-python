from rest_framework import status, generics
from rest_framework.decorators import api_view
from .models import Events
from django.contrib.auth.models import Group
from .serializers import userGroupsSerializer
from .serializers import EventsSerializer, Calenderserializer
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


class SearchEventView(generics.ListAPIView):
    """
    Search events by keywords and return events associated with the authenticated user.
    """
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        keywords = self.request.query_params.get('keywords', '')
        #case insensitive search
        print(keywords)
        return self.queryset.filter(
            Q(title__icontains=keywords) | Q(description__icontains=keywords)
        )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    


@api_view(['PUT', 'PATCH'])
def update_event(request, format=None, event_id=None):
    #Provides a method handler to update an event (PUT) or partially update an event (PATCH).

    try:
        event = Events.objects.get(pk=event_id)
    except Events.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # For PUT, update the entire event object
        serializer = EventsSerializer(event, data=request.data)
    elif request.method == 'PATCH':
        # For PATCH, update specific fields in the event object
        serializer = EventsSerializer(event, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

class CalenderView(generics.RetrieveAPIView):
    # permission_classes=[IsAuthenticated]

    queryset= Events.objects.all()
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
    
