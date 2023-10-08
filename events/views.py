from rest_framework import status
from rest_framework.decorators import api_view
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

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 