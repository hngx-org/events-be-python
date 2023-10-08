from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework import generics
from .models import Events
from users.models import CustomUser
from rest_framework import status
from rest_framework.response import Response
from .serializers import EventSerialize
from django.shortcuts import get_object_or_404
class CalenderView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    queryset= Events.objects.all()
    def retrieve(self, request, *args, **kwargs):
        events= Events.objects.filter(creator=get_object_or_404(CustomUser,name=request.user.name))
        context={}
        context['calenderDetail']=[{
            'events_start':events.start_date,
            'events_end': events.end_date,
            'time_start': events.start_time,
            'time_end':events.end_time
        } for events in events]
        return Response(context,status=status.HTTP_200_OK)

class EventDelView(generics.DestroyAPIView):
    permission_classes=[IsAuthenticated]
    queryset= Events.objects.all()
    serializer_class=EventSerialize
    lookup_field='id'
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message": "Event deleted successfully."}, status=status.HTTP_200_OK)
    


