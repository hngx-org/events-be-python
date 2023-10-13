from datetime import datetime
from django.forms import ValidationError
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
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
from social_django.models import UserSocialAuth
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema  # Import swagger_auto_schema


class CommentCreateView(APIView):
    #permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    @swagger_auto_schema(  # Add this decorator to document the view
        request_body=CommentSerializer,  # Specify the serializer for the request body
        operation_description="Create a comment with an image and voice note.",
        responses={
            201: "Comment created successfully",
            400: "Bad Request - Invalid data",
            404: "Not Found - Event not found",
            500: "Internal Server Error",
        },
    )

    def post(self, request, event_id, *args, **kwargs):
        try:
            event = get_object_or_404(Events, pk=event_id)
            current_time = datetime.utcnow()

            request.data['created_at'] = current_time
            request.data['updated_at'] = current_time
            request.data['event_id'] = event.id
            request.data['created_by'] = request.user.id

            comment = CommentSerializer(data=request.data)

            if comment.is_valid():
                comment.save()
                data = {
                    "comment": comment.data["comment"],
                    "event_id": event_id,
                }
                return Response(data, status=status.HTTP_201_CREATED)
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
