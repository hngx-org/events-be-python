from rest_framework import status
from .models import Events
from .serializers import EventsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class EventsView(APIView):
    def get(self, request, format=None):
        """
        Provides a get method handler that returns all events.
        """
        queryset = Events.objects.all()
        serializer = EventsSerializer(queryset, many=True)
        return Response(serializer.data)
