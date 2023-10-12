from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Events, InterestInEvents
from comments.models import Comment
from users.models import Group


class EventsSerializer(serializers.ModelSerializer):
    creator = serializers.UUIDField(read_only=True)
    class Meta:
        model = Events
        fields = ['id','creator','title','description','location','start_date','group','end_date', 'start_time', 'end_time', 'image']


class GetEventsSerializer(serializers.ModelSerializer):
    creator = serializers.UUIDField(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    comments_query = Comment.objects.all()

    class Meta:
        model = Events
        fields = [
            'id',
            'creator',
            'title',
            'description',
            'location',
            'start_date',
            'group',
            'end_date',
            'start_time',
            'end_time',
            'comment_count',
            'comments'
        ]

    def get_comment_count(self, obj):
        comment_count = self.comments_query.filter(event_id=obj.id).count()
        return comment_count

    def get_comments(self, obj):
        comments = self.comments_query.filter(event_id=obj.id).values(
            "comment",
            "created_at",
            "event_id",
            "created_by"
        )
        comments_list = list(comments)
        return comments_list


class Calenderserializer(serializers.ModelSerializer):
    class Meta:
        model=Events
        fields = ['id','title','start_date', 'end_date', 'start_time', 'end_time']
class userGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name') 
class userGroupsSerializerGet(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['group_name']

class InterestInEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestInEvents
        fields = '__all__'
    
