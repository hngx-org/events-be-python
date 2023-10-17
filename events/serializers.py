from django.contrib.auth.models import User, Group
from rest_framework import serializers

from users import validators
from .models import Events, InterestinEvents
from comments.models import Comment
from users.models import Group
from social_django.models import UserSocialAuth



class EventsSerializer(serializers.ModelSerializer):
    creator = serializers.UUIDField(read_only=True)
    base64_img = serializers.CharField(
        validators=[validators.validate_base64],
        required=False
        )
    image = serializers.ImageField(required=False,read_only=True)
    class Meta:
        model = Events
        fields = ['id','creator','title','description','location','start_date','group','end_date', 'start_time', 'end_time', 'image','base64_img']
    
    def create(self, validated_data):

       base64_img = validated_data.pop('base64_img')

       events = Events.objects.create(**validated_data)

       return events

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

class InterestinEventsSerializer(serializers.ModelSerializer):
    event = serializers.PrimaryKeyRelatedField(queryset=Events.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(queryset=UserSocialAuth.objects.all(), required=False)

    class Meta:
        model = InterestinEvents
        fields = '__all__'
    
