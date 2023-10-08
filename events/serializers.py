from rest_framework.serializers import ModelSerializer
from . models import Events


class EventsSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'