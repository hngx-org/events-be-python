from django.shortcuts import render
from .models import Events
from .serializers import EventsSerializer
from django.http import JsonResponse


def get_all_events(request):
    """
    Provides a get method handler that returns all events.
    """
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    return JsonResponse(serializer_class.data, safe=False)
