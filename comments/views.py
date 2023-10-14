from datetime import datetime
from django.forms import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.validators import ValidationError
from .models import Comment
from .serializers import CommentSerializer
from events.models import Events
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema  
from django.core.files.base import ContentFile  


class CommentCreateView(APIView):
    #permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=CommentSerializer,
        operation_description="Create a comment with an image, voice note, or text comment.",
        responses={
            201: "Comment created successfully",
            400: "Bad Request - Invalid data",
            404: "Not Found - Event not found",
            500: "Internal Server Error",
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            event_id = request.data.get('event_id')  # Get event_id from request.data
            event = get_object_or_404(Events, pk=event_id)
            current_time = datetime.utcnow()

            comment_data = {
                "comment": request.data.get('comment'),
                "event_id": event_id,
                "created_by": request.user.id
            }
            
            # Extract the voice note file and handle it separately
            voice_note = request.data.get('voice_note')
            picture = request.data.get('picture')

            # Check if at least one of the fields is provided
            if not any([comment_data['comment'], voice_note, picture]):
                return Response({"error": "At least one of comment, voice note, or picture must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            data = comment_data.copy()  # Create a mutable copy of comment_data
            data['created_at'] = current_time
            data['updated_at'] = current_time
            data['event'] = event.id

            comment = CommentSerializer(data=data)

            if comment.is_valid():
                comment.save()
                
                comment_instance = comment.instance

                if voice_note:
                    # Use ContentFile to properly save binary data to FileField
                    comment_instance.voice_note.save(f"{comment_instance.id}.mp3", ContentFile(voice_note.read()))
                if picture:
                    comment_instance.picture = picture
                comment_instance.save()
                
                response_data = {
                    "comment": comment_instance.comment,
                    "event_id": event_id,
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(comment.errors, status=status.HTTP_400_BAD_REQUEST)

        except Events.DoesNotExist:
            return Response({"error": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    #permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            Events.objects.get(pk=event_id)
        except (Events.DoesNotExist, ValidationError):
            return Response({"detail": "Event ID is incorrect"}, status=404)

        comments = CommentSerializer(self.queryset.filter(event_id=event_id),
                                     many=True)
        return Response(comments.data)
