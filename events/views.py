from .serializers import EventsSerializer
from . models import *
from rest_framework.generics import CreateAPIView



class CreateEventView(CreateAPIView):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer