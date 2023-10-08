
from rest_framework import status, generics
from .models import Events
from .serializers import EventsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q 
from .serializers import EventsSerializer
from . models import *
from rest_framework.generics import CreateAPIView


class CreateEventView(CreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class EventsView(APIView):
    def get(self, request, format=None):
        """
        Provides a get method handler that returns all events.
        """
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
    Search events by keywords.
    """
    queryset = Events.objects.all()
    serializer_class = EventsSerializer 

    def get_queryset(self):
        keywords = self.request.query_params.get('keywords', '')

        #case insensitive search
        return self.queryset.filter(
            Q(title__icontains=keywords) | Q(description__icontains=keywords)  
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

