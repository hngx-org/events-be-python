from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Events


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'


class userGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name') 
    