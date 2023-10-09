from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Events


class EventsSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Events
        fields = '__all__'

class Calenderserializer(serializers.ModelSerializer):
    class Meta:
        model=Events
        fields = ['start_date', 'end_date', 'start_time', 'end_time']
class userGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name') 
    