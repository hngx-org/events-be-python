from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Events


class EventsSerializer(serializers.ModelSerializer):
    creator = serializers.UUIDField(read_only=True)
    class Meta:
        model = Events
        fields = ['creator','start_date', 'end_date', 'start_time', 'end_time']

class Calenderserializer(serializers.ModelSerializer):
    class Meta:
        model=Events
        fields = ['title','start_date', 'end_date', 'start_time', 'end_time']
class userGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name') 
    