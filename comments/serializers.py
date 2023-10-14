from rest_framework import serializers


from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment', 'picture', 'voice_note', 'event_id']
        
class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class CommentpicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['picture']