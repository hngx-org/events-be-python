from datetime import datetime
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from .models import Comment
from .serializers import CommentSerializer
from events.models import Events
from users.authentication import AuthenticationMiddleware, IsAuthenticatedUser
from django.core.exceptions import ValidationError

@api_view(["POST"])
@authentication_classes([AuthenticationMiddleware])
@permission_classes([IsAuthenticatedUser])
@parser_classes([MultiPartParser, FormParser])

def create_comment(request, event_id, *args, **kwargs):
    try:
        event = get_object_or_404(Events, pk=event_id)
        current_time = datetime.utcnow()

        # Adjust the request data to include created_at, updated_at, event_id, and created_by
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

    def get(self, request, event_id):
        try:
            Events.objects.get(pk=event_id)
        except (Events.DoesNotExist, ValidationError):
            return Response({"detail": "Event ID is incorrect"}, status=404)

        comments = CommentSerializer(self.queryset.filter(event_id=event_id),
                                     many=True)
        return Response(comments.data)
