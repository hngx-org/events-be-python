from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.views import generic
from .models import Events
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class CalenderView(generic.DetailView):
    permission_classes=[IsAuthenticated]
    authentication_classes = [
        BasicAuthentication]
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        events= Events.objects.filter(id=self.request.id)
        context['calenderDetail']=[{
            'events_start':events.start_date,
            'events_end': events.end_date,
            'time_start': events.start_time,
            'time_end':events.end_time
        } for events in events]
        return Response(context,status=status.HTTP_200_OK)